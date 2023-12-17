class PromtsGenerator:
    connection_channels = {
        "TMO": "рекламный текст для колл центра (телемаркетинг)",
        "SMS": "рекламное смс-сообщение ",
        "PUSH": "рекламный текст для пуш в мобильном банке",
        "EMAIL": "рекламный текст для емэйл",
        "MOB_BANNER": "рекламный текст для баннера в мобильном приложении",
        "OFFICE_BANNER": "рекламный текст для баннера для менеджера в доп. офисе",
        "MOBILE_CHAT": "рекламный текст для предложения в чате мобильного банке",
        "KND": "рекламный текст для курьера на дом"
    }
    general_products = {
        "ПК": "Классический потребительский кредит",
        "TOPUP": "Рефинансирование внутреннего ПК в Газпромбанке",
        "REFIN": "Рефинансирование внешнего ПК в другом банке",
        "CC": "Кредитная карта",
        "AUTO": "Классический автокредит",
        "AUTO_SCR": "Кредит под залог авто",
        "MORTG": "Ипотека (обычная, льготная, ИТ, дальневосточная и тд)",
        "MORTG_REFIN": "Рефинансирование ипотеки",
        "MORTG_SCR": "Кредит под залог недвижимости",
        "DEPOSIT": "Депозит",
        "SAVE_ACC": "Накопительный счет",
        "DC": "Дебетовая карта (МИР, UNION PAY, и тд)",
        "PREMIUM": "Премиальная карта",
        "INVEST": "Брокерский и инвестиционный счет (акции, облигации, ПИФ, валюта)",
        "ISG": "Инвестиционное страхование жизни",
        "NSG": "Накопительное страхование жизни",
        "INS_LIFE": "Страхование жизни",
        "INS_PROPERTY": "Страхование жизни",
        "TRUST": "Доверительное управление",
        "OMS": "Обезличенный металлический счет",
        "IZP": "Индивидуальный зарплатный проект",
        "CURR_EXC": "Обмен валюты"
    }

    def generate_basic_promt(self, service_key, sevice_features, channel_type_key):
        service = self.general_products[service_key]
        channel_type = self.connection_channels[channel_type_key]
        promt = f"Сгенерируй {channel_type} для услуги '{service}'. {sevice_features}. "
        return promt

    def _get_user_features_text(self, service_key, user_features):
        user_feature_text = ' клиента'

        if user_features['age'] is not None:
            user_feature_text += f' {int(user_features["age"])} лет'

        if user_features['reg_region_nm'] is not None:
            user_feature_text += f' из {user_features["reg_region_nm"]}'

        if service_key == 'AUTO' or 'AUTO_SCR':
            if user_features['app_vehicle_ind'] is not None:
                user_feature_text += (' с автомобилем' if user_features['app_vehicle_ind'] else ' без автомобиля')

        if service_key == 'CC':
            if user_features['limit_exchange_count'] is not None:
                user_feature_text += f' с {user_features["limit_exchange_count"]} изменениями лимита'

        if service_key == 'TOPUP' or service_key == 'REFIN':
            if user_features['avg_outstanding_amount_3m'] is not None:
                user_feature_text += f' cо средней задолженностью по основному долгу за 3 месяца'

        return user_feature_text

    def generate_personalized_promt(self, service_key, sevice_features, channel_type_key, user_features):
        service = self.general_products[service_key]
        channel_type = self.connection_channels[channel_type_key]
        user_features_text = self._get_user_features_text(user_features)
        promt = f"Сгенерируй {channel_type} для {user_features_text}. Прорекламируй услугу '{service}'. {sevice_features}. "
        return promt

promtsgenerator = PromtsGenerator()

if __name__ == '__main__':
    promts_generator = PromtsGenerator()
    # features = 'Карта «Мир» с кэшбэком до 30%'
    # features = 'Семейная ипотека с господдержкой для семьи с детьми'
    features = 'Быстрый кредит до 7 миллионов рублей, нужен только паспорт. Ставка от 3.9% годовых'
    print(promts_generator.generate_basic_promt('ПК', features, 'SMS'))
