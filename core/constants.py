
PAYMENT_EXPIRED = "expired"
PAYMENT_PAID = "paid"
PAYMENT_FAILED = "failed"
PAYMENT_CANCELED = "canceled"
PAYMENT_IN_PROGRESS = "progress"

SUPERVISOR_TYPE = [
    (True,'Admin'),
    (False,'Supervisor')
]

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

CIB = "CIB"
EDAHABIA = "EDAHABIA"

WILAYA = [
('01', '01- Adrar'),
('02', '02- Chlef'),
('03', '03- Laghouat'),
('04', '04- Oum El Bouaghi'),
('05', '05- Batna'),
('06', '06- Bejaïa'),
('07', '07- Biskra'),
('08', '08- Béchar'),
('09', '09- Blida'),
('10', '10- Bouira'),
('11', '11- Tamanrasset'),
('12', '12- Tebessa'),
('13', '13- Tlemcen'),
('14', '14- Tiaret'),
('15', '15- Tizi Ouzou'),
('16', '16- Alger'),
('17', '17- Djelfa'),
('18', '18- Djijel'),
('19', '19- Sétif'),
('20', '20- Saïda'),
('21', '21- Skikda'),
('22', '22- Sidi Bel Abbès'),
('23', '23- Annaba'),
('24', '24- Guelma'),
('25', '25- Constantine'),
('26', '26- Médéa'),
('27', '27- Mostaganem'),
('28', '28- MSila'),
('29', '29- Mascara'),
('30', '30- Ouargla'),
('31', '31- Oran'),
('32', '32- El Bayadh'),
('33', '33- Illizi'),
('34', '34- Bordj Bou Arreridj'),
('35', '35- Boumerdès'),
('36', '36- El Tarf'),
('37', '37- Tindouf'),
('38', '38- Tissemsilt'),
('39', '39- El Oued'),
('40', '40- Khenchela'),
('41', '41- Souk Ahras'),
('42', '42- Tipaza'),
('43', '43- Mila'),
('44', '44- Aïn Defla'),
('45', '45- Naâma'),
('46', '46- Aïn Témouchent'),
('47', '47- Ghardaia'),
('48', '48- Relizane'),
('49', '49- Timimoun'),
('50', '50- Bordj Badji Mokhtar'),
('51', '51- Ouled Djellal'),
('52', '52- Béni Abbès'),
('53', '53- In Salah'),
('54', '54- In Guezzam'),
('55', '55- Touggourt'),
('56', '56- Djanet'),
('57', '57- El MGhair'),
('58', '58- El Meniaa'),
]


DELIVERY_MODE = {
    ("H", "Delivery to home"),
    ("A", "Delivery to Yalidine agency (cheaper)"),
}