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


class CardType(str, Enum):
    physical = 'physical'
    virtual = 'virtual'


class CardIssuer(str, Enum):
    accendo = 'accendo'
    cuenca = 'cuenca'


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


class CardDesign(str, Enum):
    clasica = 'clasica'
    travesia = 'travesia'
    carla = 'carla'


class CardFulfillment(str, Enum):
    new_local = 'NL'
    new_foreign = 'NF'
    replacement_mc = 'RE'
    replacement_local = 'RL'
    replacement_foreign = 'RF'
