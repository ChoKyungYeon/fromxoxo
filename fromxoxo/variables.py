
weekdaylist = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday',
]

banklist=[
    'BNK부산은행',
    'DGB대구은행',
    'IBK기업은행',
    'KB국민은행',
    'MG새마을금고',
    'SC제일은행',
    'Sh수협은행',
    '광주은행',
    '농협',
    '신한은행',
    '신협',
    '우리은행',
    '우체국은행',
    '저축은행',
    '카카오뱅크',
    '케이뱅크',
    '토스',
    '하나은행'
]

bankdictionary={
    bank: f'/static/banks/{bank}.png' for bank in banklist
}
