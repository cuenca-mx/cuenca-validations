from enum import Enum


class CardNetwork(str, Enum):
    atm = 'atm'
    visa = 'visa'


class CardStatus(str, Enum):
    active = 'active'
    blocked = 'blocked'
    created = 'created'
    deactivated = 'deactivated'
    printing = 'printing'


class CardTransactionType(str, Enum):
    auth = 'auth'
    capture = 'capture'
    expiration = 'expiration'
    refund = 'refund'
    void = 'void'
    chargeback = 'chargeback'
    fast_funds = 'fast_funds'
    push = 'push'
    push_confirmation = 'push_confirmation'


class CardFraudType(str, Enum):
    authorize = 'authorize'
    rejected = 'rejected'
    uncertain = 'uncertain'


class CardType(str, Enum):
    physical = 'physical'
    virtual = 'virtual'


class CardIssuer(str, Enum):
    accendo = 'accendo'
    cuenca = 'cuenca'


class IssuerNetwork(str, Enum):
    mastercard = 'Mastercard'
    visa = 'Visa'


class CardFundingType(str, Enum):
    credit = 'credit'
    debit = 'debit'


class DepositNetwork(str, Enum):
    cash = 'cash'
    internal = 'internal'
    spei = 'spei'


class ServiceProviderCategory(str, Enum):
    cable = 'cable'
    credit_card = 'credit_card'
    electricity = 'electricity'
    gas = 'gas'
    internet = 'internet'
    landline_telephone = 'landline_telephone'
    mobile_telephone_postpaid = 'mobile_telephone_postpaid'
    mobile_telephone_prepaid = 'mobile_telephone_prepaid'
    satelite_television = 'satelite_television'
    water = 'water'


class TransactionStatus(str, Enum):
    created = 'created'
    submitted = 'submitted'
    in_review = 'in_review'
    succeeded = 'succeeded'
    failed = 'failed'


class TransferNetwork(str, Enum):
    internal = 'internal'
    spei = 'spei'


class CommissionType(str, Enum):
    card_request = 'card_request'
    cash_deposit = 'cash_deposit'
    outgoing_spei = 'outgoing_spei'
    card_shipping = 'card_shipping'
    arteria = 'arteria'
    connect = 'connect'


class EntryType(str, Enum):
    credit = 'credit'
    debit = 'debit'


class CardErrorType(str, Enum):
    blocked = 'blocked'
    insufficient_founds = 'insufficient_founds'
    notification = 'notification'
    notification_deactivated_card = 'notification_deactivated_card'
    contactless_amount_limit = 'contactless_amount_limit'
    communication = 'communication'
    fraud_detection = 'fraud_detection'
    fraud_detection_uncertain = 'fraud_detection_uncertain'
    invalid_pin = 'invalid_pin'
    cash_advance_daily_limit = 'cash_advance_daily_limit'


class FileFormat(str, Enum):
    pdf = 'application/pdf'
    xml = 'application/xml'
    any = '*/*'


class TrackDataMethod(str, Enum):
    not_set = 'not-set'
    terminal = 'terminal'
    manual = 'manual'
    unknown = 'unknown'
    contactless = 'contactless'
    fall_back = 'fall_back'
    magnetic_stripe = 'magnetic_stripe'
    recurring_charge = 'recurring_charge'


class PosCapability(str, Enum):
    not_set = 'not-set'
    unknown = 'unknown'
    pin_accepted = 'pin_accepted'
    pin_not_accepted = 'pin_not_accepted'
    pin_pad_down = 'pin_pad_down'
    reserved = 'reserved'


class AuthorizerTransaction(str, Enum):
    advice = 'advice'
    normal_purchase = 'normal_purchase'
    cash_advance = 'cash_advance'
    returns = 'returns'
    balance_inquiry = 'balance_inquiry'
    purchase_with_cashback = 'purchase_with_cashback'
    not_defined = 'not_defined'
    mail_or_phone_order = 'mail_or_phone_order'
    change_pin = 'change_pin'
    notification = 'notification'
    card_validation = 'card_validation'
    check_out = 'check_out'
    re_authorization = 're_authorization'
    re_returns = 're_returns'
    fast_funds = 'fast_funds'
    fast_funds_reverse = 'fast_funds_reverse'


class UserCardNotification(str, Enum):
    balance_inquiry = 'balance_inquiry'
    card_blocked = 'card_blocked'
    monthly_purchases = 'monthly_purchases'


class CardDesign(str, Enum):
    classic = 'classic'
    travesia = 'travesia'
    limited_edition = 'limited_edition'


class CardPackaging(str, Enum):
    manual_local = 'NL'
    manual_nonlocal = 'NF'
    automated_local = 'RL'
    automated_nonlocal = 'RF'
    automated_batch_shipping = 'RE'


class CardholderVerificationMethod(str, Enum):
    # Describes how the cardholder verified their
    # identity (PIN, signature, with app, etc.).
    unknown = 'unknown'
    signature = 'signature'
    pin = 'pin'
    not_attended = 'not_attended'
    mail_or_phone = 'mail_or_phone'
    quick_payment_service = 'quick_payment_service'
    contactless = 'contactless'
    app_confirmation = 'app_confirmation'


class WalletTransactionType(str, Enum):
    deposit = 'deposit'
    withdrawal = 'withdrawal'


class SavingCategory(str, Enum):
    general = 'general'
    home = 'home'
    vehicle = 'vehicle'
    travel = 'travel'
    clothing = 'clothing'
    other = 'other'
    medical = 'medical'
    accident = 'accident'
    education = 'education'


class EcommerceIndicator(str, Enum):
    """
    Adquirente graba
    Emisor lee
    0, “ “ = No es una transacción de comercio electrónico
    1 = Transacción MOTO
    2 = MOTO Indicator – Recurring Transaction
    3 = MOTO Indicator – Installment Payment
    4 = MOTO Indicator – Deferred Transaction
    5 = Comercio seguro, titular autenticado (3D Secure)
    6 = Comercio seguro, titular no autenticado (3D Secure)
    7 = Autenticación 3D Secure no realizada
    8 – La transacción no incluye el uso de ningún cifrado de transacción
        como SSL, no se realiza autenticación.
    """

    not_ecommerce = '0'
    moto_transaction = '1'
    moto_recurring_transaction = '2'
    moto_installment_payment = '3'
    moto_deferred_transaction = '4'
    authenticated_3ds = '5'
    not_authenticated_3ds = '6'
    not_3ds = '7'
    not_secure_transaction = '8'


class TransactionTokenValidationStatus(str, Enum):
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'


class KYCFileType(str, Enum):
    dni = 'dni'
    ine = 'ine'
    passport = 'passport'
    residency = 'residency'
    matricula_consular = 'matricula_consular'
    proof_of_liveness = 'proof_of_liveness'
    proof_of_address = 'proof_of_address'
    rfc = 'rfc'


class Gender(str, Enum):
    female = 'female'
    male = 'male'


class State(str, Enum):
    NE = 'NE'  # Nacido en el Extranjero
    AS = 'AS'  # Aguascalientes
    BC = 'BC'  # Baja California
    BS = 'BS'  # Baja California Sur
    CC = 'CC'  # Campeche
    CS = 'CS'  # Chiapas
    CH = 'CH'  # Chihuahua
    CL = 'CL'  # Coahuila
    CM = 'CM'  # Colima
    DF = 'DF'  # Ciudad de México
    DG = 'DG'  # Durango
    GT = 'GT'  # Guanajuato
    GR = 'GR'  # Guerrero
    HG = 'HG'  # Hidalgo
    JC = 'JC'  # Jalisco
    MC = 'MC'  # México
    MN = 'MN'  # Michoacan
    MS = 'MS'  # Morelos
    NT = 'NT'  # Nayarit
    NL = 'NL'  # Nuevo León
    OC = 'OC'  # Oaxaca
    PL = 'PL'  # Puebla
    QT = 'QT'  # Querétaro
    QR = 'QR'  # Quintana Roo
    SP = 'SP'  # San Luis Potosí
    SL = 'SL'  # Sinaloa
    SR = 'SR'  # Sonora
    TC = 'TC'  # Tabasco
    TL = 'TL'  # Tlaxcala
    TS = 'TS'  # Tamaulipas
    VZ = 'VZ'  # Veracruz
    YN = 'YN'  # Yucatán
    ZS = 'ZS'  # Zacatecas


# Country enum was built with pycountry==22.1.10
# ISO 3166-1  Alpha 2
# https://github.com/flyingcircusio/pycountry/blob/af4e4a8b14388e50d5d796e7a732efd129032fd8/src/pycountry/databases/iso3166-1.json
class Country(str, Enum):
    AW = 'AW'  # Aruba
    AF = 'AF'  # Afghanistan
    AO = 'AO'  # Angola
    AI = 'AI'  # Anguilla
    AX = 'AX'  # Åland Islands
    AL = 'AL'  # Albania
    AD = 'AD'  # Andorra
    AE = 'AE'  # United Arab Emirates
    AR = 'AR'  # Argentina
    AM = 'AM'  # Armenia
    AS = 'AS'  # American Samoa
    AQ = 'AQ'  # Antarctica
    TF = 'TF'  # French Southern Territories
    AG = 'AG'  # Antigua and Barbuda
    AU = 'AU'  # Australia
    AT = 'AT'  # Austria
    AZ = 'AZ'  # Azerbaijan
    BI = 'BI'  # Burundi
    BE = 'BE'  # Belgium
    BJ = 'BJ'  # Benin
    BQ = 'BQ'  # Bonaire, Sint Eustatius and Saba
    BF = 'BF'  # Burkina Faso
    BD = 'BD'  # Bangladesh
    BG = 'BG'  # Bulgaria
    BH = 'BH'  # Bahrain
    BS = 'BS'  # Bahamas
    BA = 'BA'  # Bosnia and Herzegovina
    BL = 'BL'  # Saint Barthélemy
    BY = 'BY'  # Belarus
    BZ = 'BZ'  # Belize
    BM = 'BM'  # Bermuda
    BO = 'BO'  # Bolivia, Plurinational State of
    BR = 'BR'  # Brazil
    BB = 'BB'  # Barbados
    BN = 'BN'  # Brunei Darussalam
    BT = 'BT'  # Bhutan
    BV = 'BV'  # Bouvet Island
    BW = 'BW'  # Botswana
    CF = 'CF'  # Central African Republic
    CA = 'CA'  # Canada
    CC = 'CC'  # Cocos (Keeling) Islands
    CH = 'CH'  # Switzerland
    CL = 'CL'  # Chile
    CN = 'CN'  # China
    CI = 'CI'  # Côte d'Ivoire
    CM = 'CM'  # Cameroon
    CD = 'CD'  # Congo, The Democratic Republic of the
    CG = 'CG'  # Congo
    CK = 'CK'  # Cook Islands
    CO = 'CO'  # Colombia
    KM = 'KM'  # Comoros
    CV = 'CV'  # Cabo Verde
    CR = 'CR'  # Costa Rica
    CU = 'CU'  # Cuba
    CW = 'CW'  # Curaçao
    CX = 'CX'  # Christmas Island
    KY = 'KY'  # Cayman Islands
    CY = 'CY'  # Cyprus
    CZ = 'CZ'  # Czechia
    DE = 'DE'  # Germany
    DJ = 'DJ'  # Djibouti
    DM = 'DM'  # Dominica
    DK = 'DK'  # Denmark
    DO = 'DO'  # Dominican Republic
    DZ = 'DZ'  # Algeria
    EC = 'EC'  # Ecuador
    EG = 'EG'  # Egypt
    ER = 'ER'  # Eritrea
    EH = 'EH'  # Western Sahara
    ES = 'ES'  # Spain
    EE = 'EE'  # Estonia
    ET = 'ET'  # Ethiopia
    FI = 'FI'  # Finland
    FJ = 'FJ'  # Fiji
    FK = 'FK'  # Falkland Islands (Malvinas)
    FR = 'FR'  # France
    FO = 'FO'  # Faroe Islands
    FM = 'FM'  # Micronesia, Federated States of
    GA = 'GA'  # Gabon
    GB = 'GB'  # United Kingdom
    GE = 'GE'  # Georgia
    GG = 'GG'  # Guernsey
    GH = 'GH'  # Ghana
    GI = 'GI'  # Gibraltar
    GN = 'GN'  # Guinea
    GP = 'GP'  # Guadeloupe
    GM = 'GM'  # Gambia
    GW = 'GW'  # Guinea-Bissau
    GQ = 'GQ'  # Equatorial Guinea
    GR = 'GR'  # Greece
    GD = 'GD'  # Grenada
    GL = 'GL'  # Greenland
    GT = 'GT'  # Guatemala
    GF = 'GF'  # French Guiana
    GU = 'GU'  # Guam
    GY = 'GY'  # Guyana
    HK = 'HK'  # Hong Kong
    HM = 'HM'  # Heard Island and McDonald Islands
    HN = 'HN'  # Honduras
    HR = 'HR'  # Croatia
    HT = 'HT'  # Haiti
    HU = 'HU'  # Hungary
    ID = 'ID'  # Indonesia
    IM = 'IM'  # Isle of Man
    IN = 'IN'  # India
    IO = 'IO'  # British Indian Ocean Territory
    IE = 'IE'  # Ireland
    IR = 'IR'  # Iran, Islamic Republic of
    IQ = 'IQ'  # Iraq
    IS = 'IS'  # Iceland
    IL = 'IL'  # Israel
    IT = 'IT'  # Italy
    JM = 'JM'  # Jamaica
    JE = 'JE'  # Jersey
    JO = 'JO'  # Jordan
    JP = 'JP'  # Japan
    KZ = 'KZ'  # Kazakhstan
    KE = 'KE'  # Kenya
    KG = 'KG'  # Kyrgyzstan
    KH = 'KH'  # Cambodia
    KI = 'KI'  # Kiribati
    KN = 'KN'  # Saint Kitts and Nevis
    KR = 'KR'  # Korea, Republic of
    KW = 'KW'  # Kuwait
    LA = 'LA'  # Lao People's Democratic Republic
    LB = 'LB'  # Lebanon
    LR = 'LR'  # Liberia
    LY = 'LY'  # Libya
    LC = 'LC'  # Saint Lucia
    LI = 'LI'  # Liechtenstein
    LK = 'LK'  # Sri Lanka
    LS = 'LS'  # Lesotho
    LT = 'LT'  # Lithuania
    LU = 'LU'  # Luxembourg
    LV = 'LV'  # Latvia
    MO = 'MO'  # Macao
    MF = 'MF'  # Saint Martin (French part)
    MA = 'MA'  # Morocco
    MC = 'MC'  # Monaco
    MD = 'MD'  # Moldova, Republic of
    MG = 'MG'  # Madagascar
    MV = 'MV'  # Maldives
    MX = 'MX'  # Mexico
    MH = 'MH'  # Marshall Islands
    MK = 'MK'  # North Macedonia
    ML = 'ML'  # Mali
    MT = 'MT'  # Malta
    MM = 'MM'  # Myanmar
    ME = 'ME'  # Montenegro
    MN = 'MN'  # Mongolia
    MP = 'MP'  # Northern Mariana Islands
    MZ = 'MZ'  # Mozambique
    MR = 'MR'  # Mauritania
    MS = 'MS'  # Montserrat
    MQ = 'MQ'  # Martinique
    MU = 'MU'  # Mauritius
    MW = 'MW'  # Malawi
    MY = 'MY'  # Malaysia
    YT = 'YT'  # Mayotte
    NA = 'NA'  # Namibia
    NC = 'NC'  # New Caledonia
    NE = 'NE'  # Niger
    NF = 'NF'  # Norfolk Island
    NG = 'NG'  # Nigeria
    NI = 'NI'  # Nicaragua
    NU = 'NU'  # Niue
    NL = 'NL'  # Netherlands
    NO = 'NO'  # Norway
    NP = 'NP'  # Nepal
    NR = 'NR'  # Nauru
    NZ = 'NZ'  # New Zealand
    OM = 'OM'  # Oman
    PK = 'PK'  # Pakistan
    PA = 'PA'  # Panama
    PN = 'PN'  # Pitcairn
    PE = 'PE'  # Peru
    PH = 'PH'  # Philippines
    PW = 'PW'  # Palau
    PG = 'PG'  # Papua New Guinea
    PL = 'PL'  # Poland
    PR = 'PR'  # Puerto Rico
    KP = 'KP'  # Korea, Democratic People's Republic of
    PT = 'PT'  # Portugal
    PY = 'PY'  # Paraguay
    PS = 'PS'  # Palestine, State of
    PF = 'PF'  # French Polynesia
    QA = 'QA'  # Qatar
    RE = 'RE'  # Réunion
    RO = 'RO'  # Romania
    RU = 'RU'  # Russian Federation
    RW = 'RW'  # Rwanda
    SA = 'SA'  # Saudi Arabia
    SD = 'SD'  # Sudan
    SN = 'SN'  # Senegal
    SG = 'SG'  # Singapore
    GS = 'GS'  # South Georgia and the South Sandwich Islands
    SH = 'SH'  # Saint Helena, Ascension and Tristan da Cunha
    SJ = 'SJ'  # Svalbard and Jan Mayen
    SB = 'SB'  # Solomon Islands
    SL = 'SL'  # Sierra Leone
    SV = 'SV'  # El Salvador
    SM = 'SM'  # San Marino
    SO = 'SO'  # Somalia
    PM = 'PM'  # Saint Pierre and Miquelon
    RS = 'RS'  # Serbia
    SS = 'SS'  # South Sudan
    ST = 'ST'  # Sao Tome and Principe
    SR = 'SR'  # Suriname
    SK = 'SK'  # Slovakia
    SI = 'SI'  # Slovenia
    SE = 'SE'  # Sweden
    SZ = 'SZ'  # Eswatini
    SX = 'SX'  # Sint Maarten (Dutch part)
    SC = 'SC'  # Seychelles
    SY = 'SY'  # Syrian Arab Republic
    TC = 'TC'  # Turks and Caicos Islands
    TD = 'TD'  # Chad
    TG = 'TG'  # Togo
    TH = 'TH'  # Thailand
    TJ = 'TJ'  # Tajikistan
    TK = 'TK'  # Tokelau
    TM = 'TM'  # Turkmenistan
    TL = 'TL'  # Timor-Leste
    TO = 'TO'  # Tonga
    TT = 'TT'  # Trinidad and Tobago
    TN = 'TN'  # Tunisia
    TR = 'TR'  # Turkey
    TV = 'TV'  # Tuvalu
    TW = 'TW'  # Taiwan, Province of China
    TZ = 'TZ'  # Tanzania, United Republic of
    UG = 'UG'  # Uganda
    UA = 'UA'  # Ukraine
    UM = 'UM'  # United States Minor Outlying Islands
    UY = 'UY'  # Uruguay
    US = 'US'  # United States
    UZ = 'UZ'  # Uzbekistan
    VA = 'VA'  # Holy See (Vatican City State)
    VC = 'VC'  # Saint Vincent and the Grenadines
    VE = 'VE'  # Venezuela, Bolivarian Republic of
    VG = 'VG'  # Virgin Islands, British
    VI = 'VI'  # Virgin Islands, U.S.
    VN = 'VN'  # Viet Nam
    VU = 'VU'  # Vanuatu
    WF = 'WF'  # Wallis and Futuna
    WS = 'WS'  # Samoa
    YE = 'YE'  # Yemen
    ZA = 'ZA'  # South Africa
    ZM = 'ZM'  # Zambia
    ZW = 'ZW'  # Zimbabwe


class VerificationStatus(str, Enum):
    not_verified = 'not_verified'
    created = 'created'
    submitted = 'submitted'
    rejected = 'rejected'
    succeeded = 'succeeded'
    review_needed = 'review_needed'
    upload_again = 'upload_again'


class EventType(str, Enum):
    created = 'created'
    succeeded = 'succeeded'
    failed = 'failed'
    updated = 'updated'
    deactivated = 'deactivated'


class UserStatus(str, Enum):
    active = 'active'
    deactivated = 'deactivated'
    fraud = 'fraud'
    in_review = 'in_review'
    pld_blocked = 'pld_blocked'


class SessionType(str, Enum):
    registration = 'session.registration'
    show_card = 'session.show_card'
    account_entries = 'session.account_entries'
    download_file = 'session.download_file'
    upload_file = 'session.upload_file'


class WebhookObject(str, Enum):
    user = 'user'
    transaction = 'transaction'


class WebhookEventType(str, Enum):
    create = 'create'
    update = 'update'
    delete = 'delete'


class WebhookEvent(str, Enum):
    card_transaction_create = 'card_transaction.create'
    card_transaction_update = 'card_transaction.update'
    user_create = 'user.create'
    user_update = 'user.update'
    user_delete = 'user.delete'
    transaction_create = 'transaction.create'
    transaction_update = 'transaction.update'
    cash_deposit_create = 'cash_deposit.create'
    cash_deposit_update = 'cash_deposit.update'
    bank_account_create = 'bank_account.create'
    bank_account_update = 'bank_account.update'


class VerificationType(str, Enum):
    phone = 'phone'
    email = 'email'


class Language(str, Enum):
    en = 'en'
    es = 'es'


class PlatformType(str, Enum):
    bridge = 'bridge'
    connect = 'connect'
    spei = 'spei'


class TermsOfService(str, Enum):
    arteria = 'arteria'
    ifpe = 'ifpe'
    tarjetas_cuenca = 'tarjetas_cuenca'
    portal = 'portal'


class FileExtension(str, Enum):
    mp4 = 'mp4'
    mov = 'mov'
    v_3gpp = '3gpp'  # 3GPP
    jpg = 'jpg'
    jpeg = 'jpeg'
    png = 'png'
    pdf = 'pdf'


class BankAccountStatus(str, Enum):
    created = 'created'
    succeeded = 'succeeded'
    failed = 'failed'
