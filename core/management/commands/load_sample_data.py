"""
Management command to load sample data for J&N Building Products.
Run: python manage.py load_sample_data
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import SiteSettings, Testimonial
from products.models import Category, Product
from services.models import Service
from projects.models import Project


class Command(BaseCommand):
    help = 'Load sample data for J&N Building Products website'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('\n🔧 Loading sample data for J&N Building Products...\n'))

        # ── 1. Site Settings ──────────────────────────────────────────
        self.stdout.write('  → Creating site settings...')
        settings, _ = SiteSettings.objects.get_or_create(pk=1)
        settings.company_name = 'J&N Building Products'
        settings.tagline = 'Make Your House Smile'
        settings.phone = '+265 991 234 567'
        settings.email = 'info@jnbuildingproducts.mw'
        settings.address = 'Blantyre, Malawi'
        settings.whatsapp_number = '+265991234567'
        settings.hero_heading = 'Building Malawi\'s Future'
        settings.hero_subheading = 'Quality building products and construction services you can trust. From cement to complete construction — we\'ve got you covered.'
        settings.about_text = (
            'J&N Building Products is a trusted supplier of quality building materials '
            'and construction services in Malawi. Founded with a passion for helping '
            'Malawians build better homes, we stock a wide range of products and offer '
            'expert construction services across the country.\n\n'
            'Our motto — "Make Your House Smile" — reflects our belief that every '
            'building project deserves the best materials and skilled craftsmanship.'
        )
        settings.years_experience = 5
        settings.projects_completed = 80
        settings.happy_clients = 200
        settings.save()
        self.stdout.write(self.style.SUCCESS('     ✓ Site settings saved'))

        # ── 2. Product Categories ─────────────────────────────────────
        self.stdout.write('  → Creating product categories...')
        categories_data = [
            ('Cement & Concrete', 'bi-hexagon-fill'),
            ('Roofing', 'bi-house-fill'),
            ('Tiles & Flooring', 'bi-grid-3x3-gap-fill'),
            ('Steel & Iron', 'bi-gear-fill'),
            ('Bricks & Blocks', 'bi-bricks'),
            ('Plumbing', 'bi-droplet-fill'),
        ]
        cats = {}
        for name, icon in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=slugify(name),
                defaults={'name': name, 'icon': icon}
            )
            cats[name] = cat
        self.stdout.write(self.style.SUCCESS(f'     ✓ {len(cats)} categories created'))

        # ── 3. Products ───────────────────────────────────────────────
        self.stdout.write('  → Creating sample products...')
        products_data = [
            {
                'name': 'Portland Cement 50kg',
                'category': 'Cement & Concrete',
                'description': 'High-strength Portland cement, ideal for all construction works including foundations, walls, and slabs. Consistent quality for reliable results.',
                'specifications': 'Weight: 50kg\nGrade: 42.5N\nSetting Time: Initial 45 min, Final 10 hours\nApplication: General construction',
                'is_featured': False,
            },
            {
                'name': 'Corrugated Iron Sheets',
                'category': 'Roofing',
                'description': 'Durable galvanised corrugated iron roofing sheets. Available in multiple lengths. Rust-resistant and long-lasting for Malawian weather conditions.',
                'specifications': 'Thickness: 0.3mm, 0.4mm, 0.5mm\nLengths: 6ft, 8ft, 10ft, 12ft\nFinish: Galvanised\nColour: Silver / Pre-painted',
                'is_featured': False,
            },
            {
                'name': 'Ceramic Floor Tiles 60x60',
                'category': 'Tiles & Flooring',
                'description': 'Premium quality ceramic floor tiles. Smooth finish, scratch-resistant, and easy to clean. Perfect for living rooms, kitchens, and offices.',
                'specifications': 'Size: 60cm x 60cm\nThickness: 9mm\nFinish: Polished\nCoverage: 4 tiles per m²\nBox: 4 tiles / 1.44m²',
                'is_featured': False,
            },
            {
                'name': 'Y10 Steel Reinforcement Bars',
                'category': 'Steel & Iron',
                'description': 'High-tensile steel reinforcement bars (rebars) for reinforced concrete structures. Essential for foundations, columns, and beams.',
                'specifications': 'Diameter: 10mm (Y10)\nLength: 12 metres\nGrade: 460B\nStandard: BS 4449',
                'is_featured': False,
            },
            {
                'name': 'Hollow Concrete Blocks 6"',
                'category': 'Bricks & Blocks',
                'description': 'Machine-pressed hollow concrete blocks for fast, strong wall construction. Lightweight yet durable. Ideal for residential and commercial buildings.',
                'specifications': 'Size: 440 x 215 x 150mm (6")\nWeight: ~15kg each\nCompressive Strength: 7.5 N/mm²\nPallet: 80 blocks',
                'is_featured': False,
            },
            {
                'name': 'PVC Water Pipes (Various Sizes)',
                'category': 'Plumbing',
                'description': 'High-quality PVC pressure pipes for water supply and drainage systems. UV resistant, easy to install, and suitable for indoor and outdoor use.',
                'specifications': 'Sizes: ½", ¾", 1", 1½", 2", 3"\nLength: 3 metres per pipe\nClass: B (4 bar), C (6 bar)\nColour: Grey / White',
                'is_featured': False,
            },
        ]
        count = 0
        for data in products_data:
            cat = cats[data.pop('category')]
            slug = slugify(data['name'])
            Product.objects.get_or_create(
                slug=slug,
                defaults={**data, 'category': cat, 'image': ''}
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f'     ✓ {count} products created'))

        # ── 4. Services ───────────────────────────────────────────────
        self.stdout.write('  → Creating sample services...')
        services_data = [
            {
                'title': 'Residential Construction',
                'short_description': 'Complete home building from foundation to finishing. We handle everything — design, materials, and construction.',
                'description': 'Our residential construction service covers the complete building of homes across Malawi. From foundation laying to roofing, plastering, tiling, and final finishing — our experienced team delivers quality homes on time and within budget. We work with homeowners directly and with architects to bring your vision to life.',
                'icon': 'bi-house-fill',
                'is_featured': False,
                'order': 1,
            },
            {
                'title': 'Commercial Construction',
                'short_description': 'Office blocks, shops, warehouses, and institutional buildings constructed to the highest standard.',
                'description': 'J&N Building Products handles commercial construction projects of all sizes — from small shops to large office complexes and warehouses. We understand the importance of structural integrity, building codes, and timelines for business clients. Our team is equipped for large-scale projects with professional project management.',
                'icon': 'bi-building-fill',
                'is_featured': False,
                'order': 2,
            },
            {
                'title': 'Renovation & Remodelling',
                'short_description': 'Transform your existing space. We handle extensions, refurbishments, and full property renovations.',
                'description': 'Give your property a new lease of life with our renovation and remodelling services. Whether you need to extend your home, upgrade your kitchen, retile your floors, or completely gut and refit a commercial property — we have the skills and materials to do it professionally.',
                'icon': 'bi-tools',
                'is_featured': False,
                'order': 3,
            },
            {
                'title': 'Roofing & Waterproofing',
                'short_description': 'Expert roofing installation, repair, and waterproofing using quality materials to protect your building.',
                'description': 'Our roofing team installs, repairs, and replaces roofs for residential and commercial properties. We use quality corrugated iron sheets, tiled roofs, and flat roof systems. All our roofing work includes waterproofing to protect against Malawi\'s rainy seasons.',
                'icon': 'bi-house-gear-fill',
                'is_featured': False,
                'order': 4,
            },
            {
                'title': 'Tiling & Flooring',
                'short_description': 'Professional floor and wall tiling using quality ceramic, porcelain, and stone tiles.',
                'description': 'Our tiling team installs floor and wall tiles to a professional finish. We supply and lay a wide range of tiles — ceramic, porcelain, and natural stone — for kitchens, bathrooms, living rooms, and outdoor areas. We ensure perfectly level, grouted, and finished results every time.',
                'icon': 'bi-grid-3x3-gap',
                'is_featured': False,
                'order': 5,
            },
            {
                'title': 'Plumbing & Drainage',
                'short_description': 'Complete water supply and drainage systems installed by qualified plumbers.',
                'description': 'We provide complete plumbing and drainage solutions including water supply pipe installation, drainage systems, bathroom and kitchen fitouts, and borehole connections. Our plumbers are experienced and work with quality PVC and copper pipe systems.',
                'icon': 'bi-droplet-fill',
                'is_featured': False,
                'order': 6,
            },
        ]
        count = 0
        for data in services_data:
            slug = slugify(data['title'])
            Service.objects.get_or_create(
                slug=slug,
                defaults={**data, 'image': ''}
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f'     ✓ {count} services created'))

        # ── 5. Projects ───────────────────────────────────────────────
        self.stdout.write('  → Creating sample projects...')
        projects_data = [
            {
                'title': '4-Bedroom Family Home — Blantyre',
                'description': 'Complete construction of a 4-bedroom family home in Blantyre. Project included foundation, brick walls, roofing, tiling, plumbing, and electrical rough-in. Completed within 8 months.',
                'location': 'Blantyre',
                'client_name': 'Private Client',
                'is_featured': False,
            },
            {
                'title': 'Commercial Office Block — Limbe',
                'description': 'Construction of a 3-storey office building in Limbe. Steel-reinforced concrete structure with modern glass facade. Project managed by J&N from groundbreaking to handover.',
                'location': 'Limbe',
                'client_name': 'Corporate Client',
                'is_featured': False,
            },
            {
                'title': 'School Block Renovation — Zomba',
                'description': 'Full renovation of an aging school block including new roofing, plastering, floor tiling, new windows, and painting. Completed during school holidays to minimise disruption.',
                'location': 'Zomba',
                'client_name': 'Zomba Community School',
                'is_featured': False,
            },
            {
                'title': 'Retail Shop Construction — Lilongwe',
                'description': 'Fast-track construction of a retail shop unit in Lilongwe City Centre. Steel frame structure with tile flooring and full electrical installation. Completed in 3 months.',
                'location': 'Lilongwe',
                'client_name': 'Private Client',
                'is_featured': False,
            },
        ]
        count = 0
        for data in projects_data:
            slug = slugify(data['title'])
            Project.objects.get_or_create(
                slug=slug,
                defaults={**data, 'cover_image': ''}
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f'     ✓ {count} projects created'))

        # ── 6. Testimonials ───────────────────────────────────────────
        self.stdout.write('  → Creating sample testimonials...')
        testimonials = [
            ('Chisomo Banda', 'Homeowner, Blantyre', 'J&N built our family home from scratch. The quality is outstanding and they finished on time. We highly recommend them to anyone building in Malawi.', 5),
            ('Grace Phiri', 'Business Owner, Limbe', 'We used J&N for our office renovation. Professional, affordable, and the results exceeded our expectations. Will definitely use them again.', 5),
            ('James Mwale', 'Contractor', 'I always source my building materials from J&N. The prices are fair and the quality is consistently high. Best supplier in Blantyre.', 5),
            ('Fatima Nkosi', 'Homeowner, Zomba', 'The tiling team from J&N did an amazing job on our home. Clean, fast, and very professional. Our floors look beautiful!', 4),
        ]
        for name, role, message, rating in testimonials:
            Testimonial.objects.get_or_create(
                name=name,
                defaults={'role': role, 'message': message, 'rating': rating, 'is_active': True}
            )
        self.stdout.write(self.style.SUCCESS(f'     ✓ {len(testimonials)} testimonials created'))

        # ── Done ──────────────────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS('''
╔══════════════════════════════════════════════════╗
║  ✅  Sample data loaded successfully!             ║
║                                                  ║
║  Next steps:                                     ║
║  1. Run: python manage.py runserver              ║
║  2. Open: http://127.0.0.1:8000                  ║
║  3. Admin: http://127.0.0.1:8000/admin           ║
║  4. Upload real images for products/services     ║
╚══════════════════════════════════════════════════╝
        '''))
