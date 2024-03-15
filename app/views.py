from django.views import View
from django.shortcuts import HttpResponse
from .models import Student, Student_Finance, Student_Units, Unit_Info
import re


class UssdCallback(View):
    def post(self, request, *args, **kwargs):
        session_id = request.values.get("sessionId", None)
        serviceCode = request.values.get("serviceCode", None)
        phone_number = request.values.get("phoneNumber", None)
        text = request.values.get("text", "default")

        if text == "":
            response = 'CON Welcome to university USSD portal'
            response += 'Please enter you registration number to continue (or 0 to exit)'

        elif re.match(r"^[a-zA-Z]{3}\d{3}-\d{4}/\d{4}$", text):
            try:
                student = Student.objects.get(reg_no=text)
            except Student.DoesNotExist:
                return f'END Student with {text} number does not exist'

            response = f'CON Welcome {student.name}, chose your option:\n'
            response += '1. Student Finance\n'
            response += '2. Academics\n'
            response += '3. Feedback\n'
            response += '0. Exit'

        text = text.split('*')

        if text[-1] == '1' and len(text) == 2:
            response = 'CON Student Finance\nChose your option:\n'
            response += '1. Check balance\n'
            response += '2. Pay fees\n'
            response += '0. Exit'

        elif text[-1] == '1' and text[-2] == '1' and len(text) == 3:
            response = 'END An sms will be sent to you with your fee balance'

        elif text[-1] == '2' and text[-2] == '1' and len(text) == 3:
            student_finace = Student_Finance.objects.get(student=student)
            response = 'CON This is your current fee balance:\n'
            response += f'Balance: {student_finace.balance}\n'
            response += f'Semester fee: {student_finace.fee}\n'
            response += f'Enter amount you wish to pay'

        elif text[-3] == '1' and text[2] == '2' and len(text) == 4:
            amount = int(text[-1])
            student_finace = Student_Finance.objects.get(student=student)
            student_finace.balance -= amount
            student_finace.save()
            response = 'END Payment successful'

        elif text[-1] == '2' and len(text) == 2:
            response = 'CON Academics\nChose your option:\n'
            response += '1. Session reporting\n'
            response += '2. Register units\n'
            response += '3. Results\n'

        elif text[-1] == '1' and text[-2] == '2' and len(text) == 3:
            current_year = student.current_year
            current_semester = student.current_semester

            new_year = current_year + 1

            if current_semester == 2:
                new_semester == 1

            else:
                new_semester = 2

            response += 'CON Would you like to report for year {} semester {}?'.format(
                new_year, new_semester)
            response += '1. Yes\n'
            response += '2. No\n'

        elif text[-1] == '2' and text[-2] == '2' and len(text) == 3:
            reponse = 'CON These are the current units for this session\n'
            pass

        elif text[-1] == '2' and text[-2] == '3' and len(text) == 3:
            response = 'END An sms with you previous exam results will be sent to you'

        elif text[-1] == '3' and len(text) == 2:
            response = 'CON Feedback\nEnter your message'

        return response
