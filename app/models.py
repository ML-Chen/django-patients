from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class GlassesPrescription(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    od = models.CharField(verbose_name='OD', max_length=255, default='')
    os = models.CharField(verbose_name='OD', max_length=255, default='')
    va_right = models.CharField(verbose_name='Visual acuity right', max_length=255, blank=True, default='')
    va_left = models.CharField(verbose_name='Visual acuity right', max_length=255, blank=True, default='')
    pd = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(20), MaxValueValidator(90)],
        verbose_name='PD',
        null=True
    )
    pd_right = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(10), MaxValueValidator(45)],
        verbose_name='PD right',
        null=True
    )
    pd_left = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(10), MaxValueValidator(45)],
        verbose_name='PD left',
        null=True
    )
    outside = models.BooleanField(verbose_name='Is outside prescription', default=False)
    image = models.ImageField(upload_to='prescriptions/%Y/%m/%d', blank=True, null=True)
    image_2 = models.ImageField(upload_to='prescriptions/%Y/%m/%d', blank=True, null=True)
    nv = models.BooleanField(verbose_name='Is reading prescription', default=False, null=True)
    height = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    cc = models.CharField(max_length=255, blank=True, default='')
    notes = models.CharField(max_length=250, blank=True, default='')

    # Deprecated
    conj = models.CharField(max_length=255, blank=True, default='')
    sclera = models.CharField(max_length=255, blank=True, default='')
    tears = models.CharField(max_length=255, blank=True, default='')
    cornea = models.CharField(max_length=255, blank=True, default='')
    iris = models.CharField(max_length=255, blank=True, default='')
    antc = models.CharField(max_length=255, blank=True, default='')
    lll = models.CharField(verbose_name='lens/lids/lashes', max_length=255, blank=True, default='')

    class Meta:
        db_table = 'glasses_prescription'


class ContactLensPrescription(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    outside = models.BooleanField(verbose_name='Is outside prescription', default=False)
    image = models.ImageField(upload_to='prescriptions/%Y/%m/%d', blank=True, null=True)
    va_right = models.CharField(verbose_name='Visual acuity right', max_length=8, blank=True, help_text='E.g., 20/40')
    va_left = models.CharField(verbose_name='Visual acuity right', max_length=8, blank=True)
    notes = models.CharField(max_length=255, blank=True, default='')

    od_pwr = models.DecimalField(
        verbose_name='OD power',
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(-15), MaxValueValidator(15)],
        null=True
    )
    od_bc = models.DecimalField(
        verbose_name='OD base curve',
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(-15), MaxValueValidator(15)],
        null=True
    )
    od_dia = models.DecimalField(
        verbose_name='OD diameter',
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(-15), MaxValueValidator(15)],
        null=True
    )
    od_cyl = models.DecimalField(
        verbose_name='OD cylinder',
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(-20), MaxValueValidator(20)],
        null=True
    )
    od_axis = models.PositiveIntegerField(
        verbose_name='OD axis',
        validators=[MaxValueValidator(180)],
        null=True
    )
    os_pwr = models.DecimalField(
        verbose_name='OS power',
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(-15), MaxValueValidator(15)],
        null=True
    )
    os_bc = models.DecimalField(
        verbose_name='OS base curve',
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(-15), MaxValueValidator(15)],
        null=True
    )
    os_dia = models.DecimalField(
        verbose_name='OS diameter',
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(-15), MaxValueValidator(15)],
        null=True
    )
    os_cyl = models.DecimalField(
        verbose_name='OS cylinder',
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(-20), MaxValueValidator(20)],
        null=True
    )
    os_axis = models.PositiveIntegerField(
        verbose_name='OS axis',
        validators=[MaxValueValidator(180)],
        null=True
    )
    add = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True
    )
    color = models.CharField(max_length=25, blank=True, default='')
    brand = models.CharField(max_length=30, blank=True, default='')
    replacement_schedule = models.CharField(max_length=30, blank=True, default='')

    class Meta:
        db_table = 'contact_lens_prescription'


class ComprehensiveExam(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_created=True)
    chief_complaint = models.CharField(max_length=100, blank=True)
    history_of_past_illness = models.CharField(max_length=100, blank=True)
    color_blindness = models.CharField(max_length=100, blank=True)

    pupils_no_afferent_defect = models.BooleanField(verbose_name="No afferent defect", default=True)
    pupils_round_ou = models.BooleanField(verbose_name="Round OU", default=True)
    pupils_size = models.CharField(max_length=100, blank=True)

    cover_test = models.CharField(max_length=100, blank=True)
    iop_right = models.IntegerField(verbose_name="IOP (right)", blank=True, null=True)
    iop_left = models.IntegerField(verbose_name="IOP (left)", blank=True, null=True)
    old_prescription = models.ForeignKey(GlassesPrescription, on_delete=models.SET_NULL, blank=True, null=True, related_name='exams_with_old_prescription')
    visual_field = models.CharField(max_length=100, blank=True)
    ocular_dominance = models.CharField(
        choices=(
            ('R', _('Right')),
            ('L', _('Left'))
        ),
        max_length=10
    )
    extraocular_movement = models.CharField(max_length=100, default="safe", blank=True, null=True)
    phorias = models.CharField(max_length=100, blank=True, null=True)
    npc = models.IntegerField(verbose_name="near point of convergence", blank=True, null=True)
    dsc_right = models.IntegerField(verbose_name="DSC (right)", help_text="Visual acuity for distance vision without correction - right; 20/int", blank=True, null=True)
    dsc_left = models.IntegerField(verbose_name="DSC (left)", blank=True, null=True)
    nsc_right = models.IntegerField(verbose_name="NSC (right)", blank=True, null=True)
    nsc_left = models.IntegerField(verbose_name="NSC (left)", blank=True, null=True)

    # Slit lamp examination
    lens_lids_lashes = models.CharField(verbose_name="lens/lids/lashes", max_length=100, blank=True)
    conjunctivitis = models.CharField(max_length=100, blank=True)
    sclera = models.CharField(max_length=100, blank=True)
    tears = models.CharField(max_length=100, blank=True)
    cornea = models.CharField(max_length=100, blank=True)
    iris = models.CharField(max_length=100, blank=True)
    anterior_chamber = models.CharField(max_length=100, blank=True)

    # TODO: integrate a drawing app, something like https://nidhinp.wordpress.com/2014/02/19/paint-app-in-django/
    drawing1 = models.ImageField(blank=True, null=True)
    drawing2 = models.ImageField(blank=True, null=True)

    # Dilated fundus exam
    gtt = models.IntegerField(verbose_name="GTT", help_text="# of eye drops", blank=True, null=True)
    medication = models.CharField(max_length=100, blank=True)
    dfe_time = models.TimeField(verbose_name="DFE time", blank=True, null=True)
    bo = models.BooleanField(verbose_name="BO", help_text="direct ophthalmoscope", default=False)
    bio = models.BooleanField(verbose_name="BIO", help_text="binocular indirect ophthalmoscope", default=False)
    ninety_d_lens = models.BooleanField(verbose_name="90D lens", default=False)

    cd_right = models.DecimalField(verbose_name="C/D right", help_text="cup–disc ratio (right)", max_digits=4, decimal_places=2, blank=True, null=True)
    cd_left = models.DecimalField(verbose_name="C/D left", help_text="cup–disc ratio (left)", max_digits=4, decimal_places=2, blank=True, null=True)
    margin_right = models.CharField(default="distinct", max_length=50, blank=True)
    margin_left = models.CharField(default="distinct", max_length=50, blank=True)
    shape_right = models.CharField(default="round", max_length=50, blank=True)
    shape_left = models.CharField(default="round", max_length=50, blank=True)
    depth_right = models.CharField(max_length=50, blank=True)
    depth_left = models.CharField(max_length=50, blank=True)
    color_right = models.CharField(default="pink", max_length=50, blank=True)
    color_left = models.CharField(default="pink", max_length=50, blank=True)
    av_right = models.CharField(verbose_name="artery-to-vein ratio (right)", max_length=25, blank=True)
    av_left = models.CharField(verbose_name="artery-to-vein ratio (left)", max_length=25, blank=True)
    macular_right = models.CharField(default="clear", max_length=50, blank=True)
    macular_left = models.CharField(default="clear", max_length=50, blank=True)
    periphery_right = models.CharField(default="normal", max_length=50, blank=True)
    periphery_left = models.CharField(default="normal", max_length=50, blank=True)
    vessels_right = models.CharField(default="normal", max_length=50, blank=True)
    vessels_left = models.CharField(default="normal", max_length=50, blank=True)
    vitreous_right = models.CharField(default="clear", max_length=50, blank=True)
    vitreous_left = models.CharField(default="clear", max_length=50, blank=True)
    impressions = models.CharField(max_length=400, blank=True)
    plan = models.CharField(max_length=400, blank=True)
    return_to_office = models.CharField(max_length=300, blank=True)

    # Contact lens
    lids = models.CharField(
        max_length=15,
        choices=(
            ('TIGHT', 'Tight'),
            ('NORMAL', 'Normal'),
            ('LOOSE', 'Loose')
        ),
        blank=True
    )
    pupil_size = models.PositiveIntegerField(null=True, blank=True)
    iris_color = models.CharField(
        max_length=10,
        choices=(
            ('BROWN', 'Brown'),
            ('GRAY', 'Gray'),
            ('GREEN', 'Green'),
            ('BLUE', 'Blue')
        ),
        blank=True
    )
    notes = models.CharField(max_length=300, blank=True)
    contact_lens_prescription = models.ForeignKey(ContactLensPrescription, blank=True, null=True, on_delete=models.SET_NULL)
    # Evaluation
    good_fit = models.BooleanField(default=True)
    comfortable = models.BooleanField(default=True)
    good_vision = models.BooleanField(default=True)
    evaluation_notes = models.CharField(max_length=300, blank=True)

    signature = models.BooleanField(verbose_name="Signature: Dr. John Yin", default=True)

    class Meta:
        db_table = 'comprehensive_exam'


class Patient(models.Model):
    last_name = models.CharField(max_length=255, db_index=True)
    first_name = models.CharField(max_length=255, db_index=True)
    dob = models.DateField(verbose_name='date of birth')
    gender = models.CharField(
        choices=(
            ('F', _('Female')),
            ('M', _('Male')),
            ('N', _('Nonbinary')),
            ('U', _('Decline to state'))
        ),
        max_length=1,
        default='U'
    )
    phone = models.CharField(max_length=255)
    phone_2 = models.CharField(max_length=255, blank=True, default='')
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, default='')
    consent_hipaa = models.NullBooleanField(verbose_name="Consent to HIPAA privacy policy", default=False)
    consent_tcpa = models.NullBooleanField(verbose_name="Consent to text messages", default=False)
    diabetes = models.BooleanField()
    hypertension = models.BooleanField()
    hypercholesterolemia = models.BooleanField()
    downstairs = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}: {self.dob}'

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='Last name, first name, date of birth constraint',
                fields=['last_name', 'first_name', 'dob']
            )
        ]
        db_table = 'patient'


class Insurance(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=255, blank=True, default='')
    first_name = models.CharField(max_length=255, blank=True, default='')
    dob = models.DateField(verbose_name='date of birth')
    insurance_id = models.CharField(max_length=255, blank=True, default='')
    insurance_id_2 = models.CharField(max_length=255, blank=True, default='')
    can_call = models.BooleanField(default=False)
    called = models.BooleanField(default=False)

    class Meta:
        db_table = 'insurance'


class Glasses(models.Model):
    date = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prescription = models.ForeignKey(GlassesPrescription, on_delete=models.CASCADE)
    brand = models.CharField(max_length=255, blank=True, default='') # TODO: consider making into choices
    model = models.CharField(max_length=255, blank=True, default='')
    color = models.CharField(max_length=255, blank=True, default='')
    size = models.CharField(max_length=255, blank=True, default='')
    frame = models.CharField(max_length=255, blank=True, default='', verbose_name='Frame (deprecated)') # deprecated
    lens = models.CharField(max_length=255, blank=True, default='')
    contact_lens = models.CharField(max_length=255, blank=True, default='', verbose_name='Contact lens (deprecated)')
    tray_num = models.IntegerField(verbose_name="Tray #", validators=[MinValueValidator(800), MaxValueValidator(999)], null=True)
    price = models.CharField(max_length=255, blank=True)
    additional_comments = models.TextField(blank=True, default='')

    class Meta:
        verbose_name_plural = 'glasses'
        db_table = 'glasses'
