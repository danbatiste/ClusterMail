# ClusterMail
Email spammer with domain-specific language for the purpose of creating custom macros.
Compatible with Python versions 2.x and 3.x.

# Getting Started
#### Installation
`git clone https://github.com/danbatiste/ClusterMail`

#### Usage
ClusterMail can be run from the command line as follows.
`python ClusterMail.py CMM_path SMTP_server SMTP_port email password`

It can also be run directly, and if so will prompt the user to enter the above arguments.

# Writing CMMs
CMM is short for ClusterMail Macro.

#### Assigning Variables
`:=` is the assignment operator. It assigns a variable on the left to a Python expression on the right. If the expression is syntactically incorrect, the variable will be assigned its string representation. For example, in the third and fourth lines of `demo.cmm` we have
```
From    := Test sender
n       := 100
```
`Test sender` is syntactically incorrect in Python, therefore `From` is assigned its string representation, `"Test sender"`.
`100` is a syntactically correct expression, and so `n` is assigned the integer value of `100`.

#### BEGIN Statement
`BEGIN` begins the body of the email to be sent. The body of the email is composed of all lines following `BEGIN`.

#### Calling Variables
`{}` denotes a variable. When the email is composed, `{From}` will be substituted with the value of `From`, that being `"Test sender"`.

#### Special Variables
`Emails`, rather than being assigned to a string, will be converted to a list of emails to send to. This variable is meant to be assigned but not called.

`Subject` is the subject of the email.

`From` is the sender of the email.

`n` is the number of emails to be sent. This variable, when called, will evaluate to the current email number. `n` will increment from 1, and once it is greater than its original value it will reset back to 1 and move on to the next recipient. This mechanism is similar to that of a for loop.

`Email` is meant only to be called and not to be assigned. When called it will evaluate to the current recipient.


# Credits
ClusterMail is a collaboration between [@0xCoto](https://github.com/0xCoto) and [@danbatiste](https://github.com/danbatiste).
