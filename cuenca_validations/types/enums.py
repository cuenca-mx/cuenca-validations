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


class KYCFileType(Enum):
    ine = 'ine'
    passport = 'passport'
    residence = 'residence'
    matricula_consular = 'matricula_consular'
    proof_of_liveness = 'proof_of_liveness'
    proof_of_address = 'proof_of_address'


class Gender(Enum):
    female = 'female'
    male = 'male'


class States(Enum):
    NE = 'Nacido en el Extranjero'
    AS = 'Aguascalientes'
    BC = 'Baja California'
    BS = 'Baja California Sur'
    CC = 'Campeche'
    CS = 'Chiapas'
    CH = 'Chihuahua'
    CL = 'Coahuila'
    CM = 'Colima'
    DF = 'Ciudad de México'
    DG = 'Durango'
    GT = 'Guanajuato'
    GR = 'Guerrero'
    HG = 'Hidalgo'
    JC = 'Jalisco'
    MC = 'México'
    MN = 'Michoacan'
    MS = 'Morelos'
    NT = 'Nayarit'
    NL = 'Nuevo León'
    OC = 'Oaxaca'
    PL = 'Puebla'
    QT = 'Querétaro'
    QR = 'Quintana Roo'
    SP = 'San Luis Potosí'
    SL = 'Sinaloa'
    SR = 'Sonora'
    TC = 'Tabasco'
    TL = 'Tlaxcala'
    TS = 'Tamaulipas'
    VZ = 'Veracruz'
    YN = 'Yucatán'
    ZS = 'Zacatecas'
