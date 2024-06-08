from core.globals import LANGUAGE_EN_KEY, LANGUAGE_RU_KEY, LANGUAGE_UZ_KEY

TEMPLATE_MESSAGE = {
    LANGUAGE_EN_KEY: "Let's get started! Choose a template",
    LANGUAGE_RU_KEY: 'Начнём! Выбери шаблон',
    LANGUAGE_UZ_KEY: 'Boshlaylik! Shablonni tanlang',
}

LAYOUT_MESSAGE = {
    LANGUAGE_EN_KEY: "Excellent choice! Now let's decide on the way of overlaying, examples on the photo",
    LANGUAGE_RU_KEY: 'Отличный выбор! Теперь определимся со способом наложения, примеры на фото',
    LANGUAGE_UZ_KEY: 'Ajoyib tanlov! Endi biz bir-birining ustiga chiqish usulini, fotosuratdagi misollarni aniqlaymiz',
}

PHOTO_REQUEST_MESSAGE = {
    LANGUAGE_EN_KEY: "Will do! Now send me a photo for processing",
    LANGUAGE_RU_KEY: 'Будет сделано! Теперь отправь мне фото для обработки',
    LANGUAGE_UZ_KEY: 'Amalga oshiriladi! Endi menga qayta ishlash uchun fotosurat yuboring',
}

REQUEST_SUCCESS_MESSAGE = {
    LANGUAGE_EN_KEY: "Here's your new avatar, if you need I'm always here :)",
    LANGUAGE_RU_KEY: 'Лови свою новую аватарку, если понадоблюсь, то я всегда здесь :)',
    LANGUAGE_UZ_KEY: "Yangi avataringizni ushlang, agar kerak bo'lsa, men doim shu yerdaman :)",
}

PHOTO_PROCESSING_MESSAGE = {
    LANGUAGE_EN_KEY: "Your photo has been added to the queue, when the avatar is ready I'll send it to you :)\n\n"
                     'Place in the queue: {place}\n'
                     'Waiting time: {time}',
    LANGUAGE_RU_KEY: 'Твоё фото добавлено в очередь, когда аватарка будет готова, я тебе её отправлю :)\n\n'
                     'Место в очереди: {place}\n'
                     'Время ожидания: {time}',
    LANGUAGE_UZ_KEY: "Sizning rasmingiz navbatga qo'shiladi, avatar tayyor bo'lgach, men uni sizga yuboraman :)\n\n"
                     "Keyingi o'rin: {place}\n"
                     'Kutish vaqti: {time}',
}

PHOTO_PROCESSING_WITHOUT_QUEUE = {
    LANGUAGE_EN_KEY: "Your photo has been sent for processing, please wait for the result",
    LANGUAGE_RU_KEY: 'Твоё фото отправлено на обработку, пожалуйста, дождись результата',
    LANGUAGE_UZ_KEY: "Sizning suratingiz qayta ishlashga yuborildi, natijani kuting",
}

REQUEST_ERROR_MESSAGE = {
    LANGUAGE_EN_KEY: "Oops... something went wrong, please try again :)",
    LANGUAGE_RU_KEY: 'При обработке произошла ошибка, попробуй ещё раз :)',
    LANGUAGE_UZ_KEY: "Qayta ishlashda xatolik yuz berdi, yana urinib ko'ring :)",
}

MINUTE_TEXT = {
    LANGUAGE_EN_KEY: 'minutes',
    LANGUAGE_RU_KEY: 'минут',
    LANGUAGE_UZ_KEY: "daqiqa",
}

SECONDS_TEXT = {
    LANGUAGE_EN_KEY: 'seconds',
    LANGUAGE_RU_KEY: 'секунд',
    LANGUAGE_UZ_KEY: "soniya",
}
