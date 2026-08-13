from flask_mail import Mail, Message

mail = Mail()

def send_seller_status_email(shop_name, owner_name, seller_email, new_status):
    subject_map = {
        "Approved": "Your seller account has been approved!",
        "Rejected": "Update on your seller registration",
        "Suspended": "Your seller account has been suspended",
        "Pending": "Your seller account status update",
    }
    msg = Message(
        subject=subject_map.get(new_status, "Account status update"),
        recipients=[seller_email],
    )
    msg.body = (
        f"Hi {owner_name},\n\n"
        f"Your shop \"{shop_name}\" status has been updated to: {new_status}.\n\n"
        f"Regards,\nVloMa Team"
    )
    mail.send(msg)