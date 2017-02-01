from __future__ import print_function
from email.mime.text import MIMEText
import smtplib
import sys
import copy
import itertools

#print("List of common SMTP Servers & Ports: https://www.arclab.com/en/kb/email/list-of-smtp-and-pop3-servers-mailserver-list.html\n") #implant a list in the readme.md file
#CMM stands for "ClusterMail Macro"

def strip(line):
    if line[~0] == '\n':
        return line[:~0]
    return line

def filter_spaces(string):
    return ''.join(list(filter(lambda c: not c == ' ', string)))

def remove_empty(str_list):
    return list(filter(lambda x: not x == '', str_list))

def parse_CMM(file_path):
    #Parsed CMM
    parsed = { "vars" : { "n" : 1 } }

    #Parses CMM
    with open(file_path, 'r') as file:
        for line in file:

            words = line.split(' ')

            #Variable assignment
            if ":=" in line:
                eq = line.split(":=")
                var = ''.join(filter_spaces(eq[0]))

                if not len(remove_empty(eq[0].split(' '))) == 1:
                    print("Error: Variables must not contain spaces")
                    print("-> \"{}\"\n".format(strip(line)))


                value = ''.join(remove_empty(list(itertools.dropwhile(lambda c: c in (' ','\n') , eq[1:]))))
                try:
                    #Removes possible space or spaces after assignment operator
                    parsed["vars"].update( {var : eval(value)} )
                except:
                    parsed["vars"].update( {var : value} )
                continue

            #Stores the body of the email, but does not parse the body
            if line[:5] == "BEGIN":
                ln = file.read()
                parsed.update( {"BODY" : ""} )
                while not ln == '':
                    parsed["BODY"] += ln
                    ln = file.read()

    #Seperates Emails(str) into a list of emails, or gives error if no recipients are listed.
    try:
        parsed["vars"]["Emails"] = remove_empty(strip(parsed["vars"]["Emails"]).split(' '))
    except:
        print("Error: No recipients listed.")

    #Returns the parsed CMM with message body left unparsed
    return parsed

#Returns text(str) with variables swapped for their respective values in kwargs(dict).
def parse_text(text, kwargs):
    return text.format(**kwargs)

#Outputs a preview of the body of an email produced by a CMM to STDOUT
def preview(file_path):
    parsed = parse_CMM(file_path)
    parsed["vars"].update( {"Email" : "test@gmail.com"} )
    print(parse_text(parsed["BODY"], parsed["vars"]))


def main():
    #Prompts the user for required arguments if insuffucient arguments are given from the command line
    if not len(sys.argv[5:]):
        file_path = get_input("Enter path to the email macro: ")
        server = get_input("SMTP Server (Outgoing): ")
        port = get_input("Port (Outgoing) :")
        email = get_input("Sender Email: ")
        password = get_input("Sender Password: ")
    else:
        _, file_path, server, port, email, password = sys.argv

    #Parses the user's CMM
    parsed = parse_CMM(file_path)

    smtp_server = smtplib.SMTP(server,port)

    #Puts connection to SMTP server in TLS mode
    smtp_server.starttls()
    s.login(email, password)

    #Sends the email(s) to the recipient(s)
    m = 0
    for recipient in parsed["vars"]["Emails"]:

        #Creates deep copy of parsed CMM
        parsed_mut = copy.deepcopy(parsed)
        parsed_mut["vars"].update({ "Email" : recipient })

        for i in range(parsed["vars"]["n"]):
            i, m = i + 1, m + 1
            parsed_mut["vars"].update({ "n" : i + 1})

            #Parses the body text, creates an instance of MIMEText to email, and then appends Subject, To, and From.
            body = parse_text(parsed["BODY"], parsed_mut["vars"])
            msg = MIMEText(body)
            msg["Subject"] = parsed_mut["vars"]["Subject"]
            msg["From"] = parsed_mut["vars"]["From"]
            msg["To"] = parsed_mut["vars"]["To"]

            #Sends the email
            s.sendmail(email, recipient, msg.as_string())
            print("{}. Mail sent to {}".format(m, recipient))



if __name__ == "__main__":
    get_input = input

    if sys.version_info[:2] <= (2, 7):
        get_input = raw_input

    main()