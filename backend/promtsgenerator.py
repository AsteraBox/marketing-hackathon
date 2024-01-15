import pandas as pd


class PromtsGenerator:
    connection_channels = {
        "TMO": "рекламный текст для колл центра (телемаркетинг)",
        "SMS": "рекламное смс-сообщение ",
        "PUSH": "рекламный текст для пуш в мобильном банке",
        "EMAIL": "рекламный текст для емэйл",
        "MOB_BANNER": "рекламный текст для баннера в мобильном приложении",
        "OFFICE_BANNER": "рекламный текст для баннера для менеджера в доп. офисе",
        "MOBILE_CHAT": "рекламный текст для предложения в чате мобильного банке",
        "KND": "рекламный текст для курьера на дом",
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
        "CURR_EXC": "Обмен валюты",
    }
    df = pd.DataFrame(
        list(general_products.items()), columns=["Тип продукта", "Название продукта"]
    )
    descriptions = [
        "Нужен только паспорт. Авторизуйтесь через Госуслуги и получите возможность оформления заявки до 7 млн ₽ по одному документу. Получите кредит на дебетовую Умную карту с бесплатным обслуживанием и кешбэком до 10%. Карта выдается моментально. Получите кредит до 7 млн ₽, не выходя из дома в городах, где есть доставка",
        "Нужен только паспорт. Авторизуйтесь через Госуслуги и получите возможность оформления заявки до 7 млн ₽ по одному документу. Объедините ваши кредиты в один, выбрав комфортный срок гашения. Оформите сумму для закрытия текущих кредитов и необходимую сумму для любых целей",
        "Нужен только паспорт. Авторизуйтесь через Госуслуги и получите возможность оформления заявки до 7 млн ₽ по одному документу. Объедините ваши кредиты в один, выбрав комфортный срок гашения. Оформите сумму для закрытия текущих кредитов и необходимую сумму для любых целей",
        "Льготный период навсегда: до 180 дней. Обслуживание по кредитной карте: 0 рублей. Снятие до 50 000 ₽ в месяц без комиссии",
        "Если вам нужен кредит на автомобиль, лучше обратиться в надежный и проверенный банк. Изучите предложения и подберите удобный график и размер платежей с учетом ваших доходов и расходов. Максимальный срок 8 лет, максимальная сумма 7000000 рублей. Ставка от 2,4% на первые 30 дней с возможностью ее сохранения на весь срок кредита",
        "Кредит под залог авто. Ставка от 2,4% на первые 30 дней с возможностью ее сохранения на весь срок кредита. Максимальный срок кредитования 8 лет.",
        "Ипотека на строительство по программе с господдержкой. Без поручителя и дополнительного залога. Индивидуальный проект на строительство дома на своём участке или с покупкой земли",
        "Снижает процентную ставку по ипотеке при рождение ребёнка. Рефинансируйте кредиты на таунхаусы, квартиры в новостройках или на вторичном рынке. Допускаются заемщики до 70 лет (на дату погашения кредита). Срок кредитования от 1 до 30 лет",
        "Нужен только паспорт. Возможность оформления заявки до 15 млн ₽ по одному документу. Вероятность одобрения выше по кредитам с залогом, чем по иным кредитам. Платеж по кредитам с залогам ниже, чем по иным кредитам",
        "+1% к ставке. С Газпромбанк Привилегиями «Плюс». 15 000 ₽ минимальная сумма. Средства в безопасности. Вклады до 1,4 млн ₽ застрахованы в Агентстве по страхованию вкладов",
        "Повышенная ставка для новых клиентов в первые два месяца при открытии счета в мобильном приложении или интернет-банке. Выплата процентов каждый месяц. Дополнительная надбавка для абонентов Газпромбанк Мобайл и зарплатных клиентов. Лучший накопительный счет августа 2023 г. по версии Выберу.ру",
        "Бесплатное обслуживание без дополнительных условий. Бесплатное снятие наличных в банкоматах Газпромбанка и до 200 000 ₽ в месяц — в любых других банкоматах РФ. Переводы без комиссии на карты других банков по номеру телефона через систему быстрых платежей — до 150 000 ₽ в месяц. До 50% кэшбэк у партнеров начисляется дополнительно к программе лояльности от банка. Скидки и специальные предложения от платежной системы «Мир». 16,5% годовых на остаток по накопительному счету для новых клиентов и 5% годовых на остаток по карте с Газпромбанк Привилегиями.",
        "Бесплатное обслуживание без дополнительных условий. Счета в валюте без комиссии. Премиальный сервис: персональный менеджер, выделенная телефонная линия, Консьерж 24/7. + 0,2% годовых по вкладу Копить. Выбор программы привилегий: комфортное путешествие или спорт при выполнении условий обслуживания. В Спорт входит Фитнес-абонемент в World Class, Fitmost или X-FIT каждый месяц, Спортивная страховка с покрытием до 500000 ₽, скидки от партнеров. В Комфортное путешествие входит: Доступ в бизнес-залы аэропортов и ж/д вокзалов. 2 визита в месяц (при выполнении условий обслуживания) или 8 визитов в месяц при суммарном балансе от 6 млн ₽. Бесплатный трансфер в аэропорты и на ж/д вокзалы. Страхование семьи в путешествиях до 1 000 000 $",
        "Индивидуальный инвестиционный счет. Получите доход от ценных бумаг и налоговые льготы от государства. ИИС в сервисе Газпромбанк Инвестиции: открытие и управление онлайн,возможность участвовать в IPO, доступ к СПБ Бирже, топ рекомендуемых бумаг",
        "Вы заключаете договор со страховой компанией. Страховая компания направляет ваши деньги в стратегию инвестирования. На протяжении действия договора ваша жизнь и здоровье застрахованы: при наступлении сложных жизненных обстоятельств страховая компания осуществляет страховую выплату. Когда срок договора закончится, вы вернете свои вложения в полном объеме с учетом гарантированной страховой суммы (ГСС) в размере 100%. Возврат вложенных денег независимо от результатов инвестирования в конце срока договора. При оформлении договора от 5 лет вы можете получить возврат налога в размере 13% от суммы вложений, но не более 19 500 ₽",
        "Не является имуществом. Страховые накопления не подлежат разделу при разводе супругов. Адресность выплат. При наступлении страхового случая деньги выплачиваются указанному в договоре получателю без ожидания вступления в наследство. Защита средств. На протяжении действия договора деньги не могут быть конфискованы или арестованы. Возврат налога 13%. Возможность ежегодно получать возврат налога — 13% от суммы взноса (но не более 19 500 ₽ в год)",
        "Комплексное обследование вашего здоровья. Профилактическое обследование общего состояния здоровья. Своевременное обнаружение и диагностика проблем со здоровьем. Большой спектр медицинских услуг, лечение онкологических заболеваний (в случае первичного выявления). Возможность воспользоваться услугой не дожидаясь страхового события",
        "Пожар, взрыв, затопление. Возмещение ущерба в случае пожаре, взрыва, поджога и удара молнии. Стихийные бедствия. Компенсация стоимости повреждений, возникших в результате ливня, паводков, оползней и прочих опасностей. Противоправные действия 3-х лиц. Покрытие ущерба, нанесенного третьими лицами: разбитые окна, кражи со взломом, порча имущества и вандализм",
        "Группа Газпромбанка предоставляет частным инвесторам полный спектр инвестиционных услуг, отличающихся соотношением риска и доходности и полностью соответствующих их финансовым целям и задачам и зачастую не ограничен стандартными инвестиционными инструментами. Рекомендации при формировании инвестиционного портфеля основаны на детальном анализе рыночной конъюнктуры в каждом конкретном случае, и фундаментальном понимании командой тенденций развития глобальной экономики. Доверительное управление осуществляется как на основе ряда базовых инвестиционных стратегий, так и на основе стратегий, учитывающих индивидуальные предпочтения клиентов и соотношение риска и доходности. При этом подход, применяемый при разработке уникальных стратегий доверительного управления, ориентирован на детальное информирование клиента о ходе инвестиционного процесса и возможность обсуждения выбранных стратегий в любой момент времени. ",
        "Банковский счет в драгоценных металлах – это аналог текущего счета, на котором вместо денег хранится драгоценный металл в граммах. Один счет – один драгоценный металл. Проценты по счету не начисляются и не выплачиваются. Доходность определяется повышением курса драгоценного металла",
        "Выгода с зарплатной картой Газпромбанка. Дополнительный кешбэк от партнёров до 50%. Надбавка 0,2% по вкладам в рублях «Копить» и «Управлять». Надбавка 0,3% по Накопительному счету. Скидка до 2,5% по кредиту на покупку авто. Скидка до 2,8% по ипотечным программам",
        "Вы можете открыть счета в 7 валютах и обменивать деньги онлайн. Дополнительные скидки. При обмене более 1 000 единиц иностранной валюты, а также специальный курс в мобильном приложении и интернет-банке для клиентов Премиум и Private. Карта UnionPay. Закажите карту и получите доступ к обмену валюты в мобильном приложении и покупкам в 150+ странах мира. Без комиссии. Не нужно платить за хранение остатков на счетах. Специальный курс с подпиской Газпром Бонус при обмене валюты в офисе безналичным способом. Праздничный курс на покупку наличных. Покупайте наличные CNY, USD и EURO в офисах банка по сниженному курсу. Акция действует до 31 января 2024 года*. Высокий процент при открытии вклада в юанях",
    ]
    df["Описание продукта"] = descriptions

    def generate_basic_promt(self, service_key, channel_type_key):
        row = self.df[self.df["Тип продукта"] == service_key].iloc[0]
        service = row["Название продукта"]
        service_description = row["Описание продукта"]
        channel_type = self.connection_channels[channel_type_key]
        prompt = f"Сгенерируйте {channel_type} для услуги '{service}'. {service_description}. "

        return prompt

    def _get_user_features_text(self, service_key, user_features):
        user_feature_text = " клиента"

        if user_features["user_data"].age is not None:
            age = user_features["user_data"].age
            user_feature_text += f" {int(age)} лет"

        if user_features["user_data"].reg_region_nm is not None:
            reg_region_nm = user_features["user_data"].reg_region_nm
            user_feature_text += f" из {reg_region_nm}"

        if service_key == "AUTO" or "AUTO_SCR":
            if user_features["user_data"].app_vehicle_ind is not None:
                user_feature_text += (
                    " с автомобилем"
                    if user_features["user_data"].app_vehicle_ind
                    else " без автомобиля"
                )

        if service_key == "CC":
            if user_features["user_data"].limit_exchange_count is not None:
                limit = user_features["user_data"].limit_exchange_count
                user_feature_text += f" с {limit} изменениями лимита"

        if service_key == "TOPUP" or service_key == "REFIN":
            if user_features["user_data"].avg_outstanding_amount_3m is not None:
                avg_outstanding_amount_3m = user_features[
                    "user_data"
                ].avg_outstanding_amount_3m
                user_feature_text += f" cо средней задолженностью по основному долгу за 3 месяца: {avg_outstanding_amount_3m}"

        return user_feature_text

    def generate_personalized_promt(self, service_key, channel_type_key, user_features):
        row = self.df[self.df["Тип продукта"] == service_key].iloc[0]
        service = row["Название продукта"]
        service_description = row["Описание продукта"]
        channel_type = self.connection_channels[channel_type_key]
        user_features_text = self._get_user_features_text(service_key, user_features)
        promt = f"Сгенерируй {channel_type} для {user_features_text}. Прорекламируй услугу '{service}'. {service_description}. "
        return promt


promtsgenerator = PromtsGenerator()

if __name__ == "__main__":
    promts_generator = PromtsGenerator()
    # features = 'Карта «Мир» с кэшбэком до 30%'
    # features = 'Семейная ипотека с господдержкой для семьи с детьми'
    features = "Быстрый кредит до 7 миллионов рублей, нужен только паспорт. Ставка от 3.9% годовых"
    print(promts_generator.generate_basic_promt("ПК", features, "SMS"))
