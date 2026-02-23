from decimal import Decimal
from django.db import migrations


def create_test_data(apps, schema_editor):
    Profile = apps.get_model('profiles', 'Profile')
    Car = apps.get_model('cars', 'Car')
    Part = apps.get_model('repairs', 'Part')
    Repair = apps.get_model('repairs', 'Repair')
    RepairPart = apps.get_model('repairs', 'RepairPart')
    Invoice = apps.get_model('repairs', 'Invoice')

    # --- Profiles ---
    ivan = Profile.objects.create(
        first_name='Ivan', last_name='Petrov',
        email='ivan.petrov@gmail.com', phone_number='+359888123456'
    )
    maria = Profile.objects.create(
        first_name='Maria', last_name='Georgieva',
        email='maria.georgieva@abv.bg', phone_number='+359877654321'
    )
    stefan = Profile.objects.create(
        first_name='Stefan', last_name='Dimitrov',
        email='stefan.dimitrov@gmail.com', phone_number='+359899111222'
    )

    # --- Cars ---
    bmw = Car.objects.create(
        brand='BMW', model='5 Series', plate='CB1234AB',
        year=2018, engine_type='Diesel', mileage=85000, owner=ivan
    )
    audi = Car.objects.create(
        brand='Audi', model='A4', plate='PB5678CB',
        year=2020, engine_type='Gasoline', mileage=45000, owner=maria
    )
    mercedes = Car.objects.create(
        brand='Mercedes', model='C220', plate='CA9012EK',
        year=2016, engine_type='Diesel', mileage=120000, owner=stefan
    )
    vw = Car.objects.create(
        brand='Volkswagen', model='Golf 7', plate='BT3456CM',
        year=2019, engine_type='Gasoline', mileage=67000, owner=ivan
    )
    # Car without owner — for testing unassigned cars view
    Car.objects.create(
        brand='Volvo', model='XC60', plate='EB7890AM',
        year=2021, engine_type='Hybrid', mileage=23000, owner=None
    )

    # --- Parts ---
    oil_filter = Part.objects.create(
        name='Oil Filter',
        category='Engine and Transmission',
        description='High-quality oil filter compatible with most petrol and diesel engines.'
    )
    brake_pads = Part.objects.create(
        name='Front Brake Pads',
        category='Brakes and Wheels',
        description='Ceramic front brake pads, low dust, low noise formula.'
    )
    air_filter = Part.objects.create(
        name='Air Filter',
        category='Engine and Transmission',
        description='Engine air intake filter, OEM quality replacement.'
    )
    spark_plugs = Part.objects.create(
        name='Spark Plugs Set',
        category='Engine and Transmission',
        description='Iridium spark plugs set of 4, long service life.'
    )
    Part.objects.create(
        name='Timing Belt Kit',
        category='Engine and Transmission',
        description='Complete timing belt kit including tensioner and idler pulley.'
    )
    brake_disc = Part.objects.create(
        name='Front Brake Disc',
        category='Brakes and Wheels',
        description='Ventilated front brake disc, high carbon formula for better heat dissipation.'
    )
    shock_absorber = Part.objects.create(
        name='Front Shock Absorber',
        category='Suspension and Steering',
        description='Gas-pressurized front shock absorber, OEM spec.'
    )
    Part.objects.create(
        name='Power Steering Fluid',
        category='Suspension and Steering',
        description='Synthetic power steering fluid, 1L bottle.'
    )

    # --- Repairs ---

    # 1. Ivan's BMW — Oil Change — Draft
    repair_bmw = Repair.objects.create(
        category='Engine and Transmission',
        description='Regular oil change and filter replacement. Customer reports slight oil consumption.',
        status='Draft',
        labor_hours=Decimal('0.5'),
        price_per_labor_hour=Decimal('40.00'),
        car=bmw,
        is_invoiced=False
    )
    RepairPart.objects.create(repair=repair_bmw, part=oil_filter, quantity=1, price=Decimal('15.00'))

    # 2. Maria's Audi — Full Brake Service — In Progress
    repair_audi = Repair.objects.create(
        category='Brakes and Wheels',
        description='Full front brake service. Pads and discs worn beyond safe limits.',
        status='In Progress',
        labor_hours=Decimal('2.0'),
        price_per_labor_hour=Decimal('50.00'),
        car=audi,
        is_invoiced=False
    )
    RepairPart.objects.create(repair=repair_audi, part=brake_pads, quantity=2, price=Decimal('55.00'))
    RepairPart.objects.create(repair=repair_audi, part=brake_disc, quantity=2, price=Decimal('85.00'))

    # 3. Stefan's Mercedes — Engine Tune-up — Completed + Invoiced
    # labor: 1.5 * 60.00 = 90.00
    # parts: air_filter 25.00 + spark_plugs 45.00 = 70.00
    # total: 160.00
    repair_mercedes = Repair.objects.create(
        category='Engine and Transmission',
        description='Full engine tune-up. Air filter and spark plugs replaced. Idle smoothed out.',
        status='Completed',
        labor_hours=Decimal('1.5'),
        price_per_labor_hour=Decimal('60.00'),
        car=mercedes,
        is_invoiced=True
    )
    RepairPart.objects.create(repair=repair_mercedes, part=air_filter, quantity=1, price=Decimal('25.00'))
    RepairPart.objects.create(repair=repair_mercedes, part=spark_plugs, quantity=1, price=Decimal('45.00'))

    Invoice.objects.create(
        invoice_number='5847362910',
        repair=repair_mercedes,
        owner=stefan,
        total_amount=Decimal('160.00')
    )

    # 4. Ivan's VW — Suspension Repair — In Progress
    repair_vw = Repair.objects.create(
        category='Suspension and Steering',
        description='Front suspension inspection. Both front shock absorbers leaking, replacement required.',
        status='In Progress',
        labor_hours=Decimal('3.0'),
        price_per_labor_hour=Decimal('50.00'),
        car=vw,
        is_invoiced=False
    )
    RepairPart.objects.create(repair=repair_vw, part=shock_absorber, quantity=2, price=Decimal('120.00'))

    # 5. Stefan's Mercedes — Electrical Diagnostic — Cancelled
    Repair.objects.create(
        category='Electrical System',
        description='Customer reported intermittent dashboard warning lights. Diagnostic cancelled — customer declined service.',
        status='Cancelled',
        labor_hours=Decimal('0.0'),
        price_per_labor_hour=Decimal('0.00'),
        car=mercedes,
        is_invoiced=False
    )


def delete_test_data(apps, schema_editor):
    Car = apps.get_model('cars', 'Car')
    Profile = apps.get_model('profiles', 'Profile')
    Part = apps.get_model('repairs', 'Part')

    # Deleting cars cascades to Repairs → RepairParts → Invoices
    Car.objects.filter(plate__in=[
        'CB1234AB', 'PB5678CB', 'CA9012EK', 'BT3456CM', 'EB7890AM'
    ]).delete()

    Profile.objects.filter(email__in=[
        'ivan.petrov@gmail.com',
        'maria.georgieva@abv.bg',
        'stefan.dimitrov@gmail.com',
    ]).delete()

    Part.objects.filter(name__in=[
        'Oil Filter', 'Front Brake Pads', 'Air Filter',
        'Spark Plugs Set', 'Timing Belt Kit', 'Front Brake Disc',
        'Front Shock Absorber', 'Power Steering Fluid',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0004_alter_invoice_repair'),
        ('cars', '0002_alter_car_brand_alter_car_engine_type'),
    ]

    operations = [
        migrations.RunPython(create_test_data, delete_test_data),
    ]
