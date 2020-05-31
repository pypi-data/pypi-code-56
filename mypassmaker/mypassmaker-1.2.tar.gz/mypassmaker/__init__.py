class Password:
    @staticmethod
    def generate(length=8):
        import string
        import random
        char = string.ascii_letters + string.punctuation + string.digits
        final_password = "".join(random.choice(char) for x in range(int(length)))
        return final_password

    @staticmethod
    def send_email(gmail_user, gmail_password, sent_from, send_to, content):
        try:
            import smtplib
        except ImportError:
            raise Exception("Please first install smtplib via: pip install smtplib")
        subject = "Here's Your Secure password"
        print(content)

        email_text = "From: {}\nTo: {}\nSubject: {}\n This is your password: {}".format(sent_from, send_to, subject, content)
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, send_to, email_text)
            server.close()
            return True
        except smtplib.SMTPAuthenticationError:
            return False
        except smtplib.SMTPConnectError:
            return False

    @staticmethod
    def is_secure(password):
        """
            checks if given password is safe based on these parameters:
            - length is more than 8 character
            - it has lower case character
            - contains upper case characters
            - contains digit
            - contains special character
        """
        lower_case, upper_case, digit, special_character = 0, 0, 0, 0
        min_length = 8
        if len(password) >= min_length:
            for character in password:
                # counting lowercase alphabets  
                if character.islower():
                    lower_case += 1
                # counting uppercase alphabets
                elif character.isupper():
                    upper_case += 1
                # counting digits
                elif character.isdigit():
                    digit += 1
                # counting the mentioned special characters
                elif character in ['@', '$', '_', '.', '-', '&', '!', '#', '%', '^', '*', '(', ')', '+', '=']:
                    special_character += 1
            if lower_case >= 1 and upper_case >= 1 and digit >= 1 and special_character >= 1:
                return True
            else:
                return False
        else:
            return False
