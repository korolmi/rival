from django.contrib import admin

from .models import ContentEl,CatalogEl,PhotoEl,TextLabel,PageTag,ShortContentEl,OrderMsg

admin.site.register(PageTag)
admin.site.register(CatalogEl)
admin.site.register(PhotoEl)

class ContentAdmin ( admin.ModelAdmin ):

	list_display = ( 'id', 'el_level', 'el_lang', 'el_ord_no', 'el_slug', 'el_title', 'el_parent')
	list_filter = [ 'el_level', 'el_lang', ('el_parent',admin.RelatedOnlyFieldListFilter) ]
	search_fields = [ 'el_title', 'id' ]
	filter_horizontal = ("el_tags",)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "el_parent":
			kwargs["queryset"] = ContentEl.objects.filter(el_level=1)
		return super(ContentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ShortContentAdmin ( admin.ModelAdmin ):

	class Media: 
		js = ( 'jquery.js',
			'codemirror.js',
			'closebrackets.js',
			'closetag.js',
			'css.js',
			'fullscreen.js',
			'htmlmixed.js',
			'javascript.js',
			'matchbrackets.js',
			'matchtags.js',
			'xml-fold.js',
			'xml.js',
			'cdmr_conf.js',)
		css = {
			'all' : ('codemirror.css', 'fullscreen.css', 'cobalt.css')
		}

	list_display = ( 'id', 'el_level', 'el_lang', 'el_ord_no', 'el_slug', 'el_title', 'el_parent')
	list_filter = [ 'el_level', 'el_lang', ('el_parent',admin.RelatedOnlyFieldListFilter) ]
	search_fields = [ 'el_title', 'id' ]
	filter_horizontal = ("el_tags",)
	exclude = ["el_parent", "el_level", "el_ord_no", "el_lang", "el_meta_title", "el_meta_kwords", "el_type", "el_cre_date", "el_as_html", "el_templ_name", "el_page_color"]

class LabelAdmin ( admin.ModelAdmin ):

	list_display = ( 'id', 'tl_lang', 'tl_category', 'tl_name', 'tl_text')
	list_filter = [ 'tl_category', 'tl_lang' ]
	search_fields = [ 'tl_text', 'tl_name' ]

class OrderAdmin ( admin.ModelAdmin ):

	list_display = ( 'id', 'ord_cre_date', 'ord_type', 'ord_subj', 'ord_cont', 'ord_lang')
	list_filter = [ 'ord_type', 'ord_lang' ]
	search_fields = [ 'ord_cont', 'ord_subj', 'ord_details' ]

admin.site.register(ContentEl,ContentAdmin)
admin.site.register(ShortContentEl,ShortContentAdmin)
admin.site.register(TextLabel,LabelAdmin)
admin.site.register(OrderMsg,OrderAdmin)
