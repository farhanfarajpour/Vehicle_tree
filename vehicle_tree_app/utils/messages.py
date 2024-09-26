
# TODO - If you need dynamic messaging you should add table this message and error_code

class ErrorMessage:
    errors = {
        0: "This error must be handled by us.",
        1: "متأسفانه، یک مشکل فنی در سرور وجود دارد. لطفاً چند دقیقه دیگر تلاش کنید یا با پشتیبانی سایت تماس بگیرید",
        2: "نام کاربری یا رمز عبور اشتباه می باشد",
        3: "کاربر مورد نظر از قبل خروج کرده است",
        4: "آیتم مورد نظر یافت نشد",
        5: "مشکلی در افزودن آیتم رخ داده است",
        6: "مشکی در آپلود عکس رخ داده است"
    }


class SuccessMessage:
    success = {
        2000: "User information has been successfully registered.",
        2001: "خروج با موفقیت انحام شد",
        2002: "آیتم جدید با موفقیت ذخیره شد",
        2003: "آیتم مورد نظر با موفقیت آپدیت شد",
        2004: "آیتم مورد نظر با موفقیت حذف شد",
        2005: "عکس مورد نظر با موفقیت آپلود شد"
    }
