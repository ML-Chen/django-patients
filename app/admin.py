from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from .models import Patient, Insurance, Glasses, GlassesPrescription, ContactLensPrescription, ComprehensiveExam


admin.site.disable_action('delete_selected')


class InsuranceInline(admin.TabularInline):
    model = Insurance
    extra = 0


class GlassesInline(admin.TabularInline):
    model = Glasses
    raw_id_fields = ['prescription']
    extra = 0


class GlassesPrescriptionInline(admin.StackedInline):
    model = GlassesPrescription
    extra = 0


class ContactLensPrescriptionInline(admin.TabularInline):
    model = ContactLensPrescription
    extra = 0


class ComprehensiveExamInline(admin.StackedInline):
    model = ComprehensiveExam
    extra = 0


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'dob', 'phone', 'phone_2']
    inlines = [
        InsuranceInline,
        GlassesInline,
        GlassesPrescriptionInline,
        ContactLensPrescriptionInline,
        ComprehensiveExamInline
    ]
    actions = ['mark_not_here', 'mark_here']
    list_filter = ['here']

    def mark_not_here(self, request, queryset):
        rows_updated = queryset.update(here=False)
        if rows_updated == 1:
            message_bit = "1 patient was"
        else:
            message_bit = "%s patients were" % rows_updated
        self.message_user(request, "%s successfully marked as *not* here." % message_bit)
    mark_not_here.short_description = 'Mark selected patients as *not* here'

    def mark_here(self, request, queryset):
        rows_updated = queryset.update(here=True)
        if rows_updated == 1:
            message_bit = "1 patient was"
        else:
            message_bit = "%s patients were" % rows_updated
        self.message_user(request, "%s successfully marked as here." % message_bit)
    mark_here.short_description = 'Mark selected patients as here'


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

    raw_id_fields = ['patient', 'prescription']


@admin.register(GlassesPrescription)
class GlassesPrescriptionAdmin(admin.ModelAdmin):
    raw_id_fields = ['patient']


@admin.register(ContactLensPrescription)
class ContactLensPrescriptionAdmin(admin.ModelAdmin):
    raw_id_fields = ['patient']


@admin.register(ComprehensiveExam)
class ComprehensiveExamAdmin(admin.ModelAdmin):
    raw_id_fields = ['patient']

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


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    raw_id_fields = ['patient']
