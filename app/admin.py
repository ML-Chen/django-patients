from django.contrib import admin
from .models import Patient, Insurance, Glasses, GlassesPrescription, ContactLensPrescription, ComprehensiveExam


class InsuranceInline(admin.TabularInline):
    model = Insurance


class GlassesInline(admin.TabularInline):
    model = Glasses


class GlassesPrescriptionInline(admin.TabularInline):
    model = GlassesPrescription


class ContactLensPrescriptionInline(admin.TabularInline):
    model = ContactLensPrescription


class ComprehensiveExamInline(admin.TabularInline):
    model = ComprehensiveExam


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'date_of_birth', 'phone', 'phone_2']
    inlines = [InsuranceInline, GlassesInline, GlassesPrescriptionInline, ContactLensPrescriptionInline, ComprehensiveExamInline]


@admin.register(Glasses)
class GlassesAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('date', 'od', 'os', 'va_right', 'va_left', 'pd', 'outside', 'image', '')
        }),
        ('Deprecated (use Comprehensive Exam instead)', {
            'fields': ('conj', 'sclera', 'tears', 'cornea', 'iris', 'antc', 'lll')
        })
    )


@admin.register(GlassesPrescription)
class GlassesPrescriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactLensPrescription)
class ContactLensPrescriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(ComprehensiveExam)
class ComprehensiveExamAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('time', 'chief_complaint', 'history_of_past_illness', 'color_blindness')
        }),
        ('Pupils', {
            'fields': ('pupils_no_afferent_defect', 'pupils_round_ou', 'pupils_size')
        }),
        (None, {
            'fields': ('cover_test', ('iop_right', 'iop_left'), 'old_prescription', 'visual_field', 'ocular_dominance', 'extraocular_movement', 'phorias', 'npc', ('dsc_right', 'dsc_left'), ('nsc_right', 'nsc_left'))
        }),
        ('Slit lamp examination', {
            'fields': ('lens_lids_lashes', 'conjunctivitis', 'sclera', 'tears', 'cornea', 'iris', 'anterior_chamber')
        }),
        ('Sketches', {
            'fields': ('drawing1', 'drawing2')
        }),
        ('Dilated fundus exam', {
            'fields': ('gtt', 'medication', 'dfe_time', 'bo', 'bio', 'ninety_d_lens')
        }),
        (None, {
            'fields': (('cd_right', 'cd_left'), ('margin_right', 'margin_left'), ('shape_right', 'shape_left'), ('depth_right', 'depth_left'), ('color_right', 'color_left'), ('av_right', 'av_left'), ('macular_right', 'macular_left'), ('periphery_right', 'periphery_left'), ('vessels_right', 'vessels_left'), ('vitreous_right', 'vitreous_left'), 'impressions', 'plan', 'return_to_office')
        }),
        ('Contact lens', {
            'fields': ('lids', 'pupil_size', 'iris_color', 'notes', 'contact_lens_prescription', 'good_fit', 'comfortable', 'good_vision', 'evaluation_notes')
        }),
        (None, {
            'fields': ('signature',)
        })
    )
