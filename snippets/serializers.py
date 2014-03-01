from django.forms import widgets
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Snippet
        fields  = ('id', 'title', 'code', 'linenos', 'language', 'style')
        
    pk         = serializers.Field() # Note: `Field` is an untyped read-only field.
    title      = serializers.CharField(required=False,max_length=100)
    code       = serializers.CharField(widget=widgets.Textarea,max_length=100000)
    linenos    = serializers.BooleanField(required=False)
    language   = serializers.ChoiceField(choices=LANGUAGE_CHOICES,default='python')
    style      = serializers.ChoiceField(choices=STYLE_CHOICES,default='friendly')

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance, given a dict
        of deserialized field values.

        Note that if we don't define this method, then 
        deserealizing data will simply return a dict of items.
        """
        if instance:
            # Update existing instance
            instance.title      = attrs.get('title', instance.title)
            instance.code       = attrs.get('code', instance.code)
            instance.linenos    = attrs.get('linenos', instance.linenos)
            instance.language   = attrs.get('language', instance.language)
            instance.style      = attrs.get('style', instance.style)
            return instance

        # Create new instance
        return Snippet(**attrs)