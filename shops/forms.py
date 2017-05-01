from django import forms
from django.db.models import Q

from django.forms.widgets import Textarea, PasswordInput
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import ModelChoiceField
from django.contrib.auth.models import Group

from shops.models import (Shop, Container, ProductBase, ProductUnit,
                          ContainerCase)
from users.models import User
from borgia.validators import autocomplete_username_validator


class ProductCreateForm(forms.Form):
    def __init__(self, **kwargs):
        shop = kwargs.pop('shop')
        super(ProductCreateForm, self).__init__(**kwargs)
        if shop:
            self.fields['product_base'] = forms.ModelChoiceField(
                label='Base produit', queryset=ProductBase.objects.filter(
                    shop=shop, is_active=True).exclude(pk=1).order_by('name'),
                widget=forms.Select(
                    attrs={'class': 'selectpicker form-control',
                           'data-live-search': 'True'}))
        else:
            self.fields['product_base'] = forms.ModelChoiceField(
                label='Base produit', queryset=ProductBase.objects.filter(
                    is_active=True).exclude(pk=1).order_by('name'),
                widget=forms.Select(
                    attrs={'class': 'selectpicker form-control',
                           'data-live-search': 'True'}))
        self.fields['quantity'] = forms.IntegerField(
            label='Quantité à ajouter (de Fût, en KG, ou de bouteille)',
            min_value=0, max_value=5000)
        self.fields['price'] = forms.DecimalField(
            label='Prix d\'achat TTC (par Fût, KG, bouteille)',
            decimal_places=2, max_digits=9, min_value=0)
        self.fields['purchase_date'] = forms.DateField(
            label='Date d\'achat',
            widget=forms.DateInput(attrs={'class': 'datepicker'}))
        self.fields['expiry_date'] = forms.DateField(
            label='Date d\'expiration', required=False,
            widget=forms.DateInput(attrs={'class': 'datepicker'}))
        self.fields['place'] = forms.CharField(max_length=255,
                                               label='Lieu de stockage')


class ProductBaseCreateForm(forms.Form):
    def __init__(self, **kwargs):
        shop = kwargs.pop('shop')
        super(ProductBaseCreateForm, self).__init__(**kwargs)

        if shop:
            self.fields['type'] = forms.ChoiceField(
                label='Type de produit',
                choices=(('container', 'Conteneur'),
                         ('single_product', 'Produit unitaire'))
            )
            self.fields['product_unit'] = forms.ModelChoiceField(
                label='Unité de produit',
                queryset=ProductUnit.objects.filter(
                    shop=shop, is_active=True).exclude(pk=1),
                required=False,
                widget=forms.Select(
                    attrs={'class': 'selectpicker form-control',
                           'data-live-search': 'true'})
            )
        else:
            self.fields['shop'] = forms.ModelChoiceField(
                label='Magasin',
                queryset=Shop.objects.all().exclude(pk=1)
            )
            self.fields['type'] = forms.ChoiceField(
                label='Type de produit',
                choices=(('container', 'Conteneur'),
                         ('single_product', 'Produit unitaire'))
            )
            self.fields['product_unit'] = forms.ModelChoiceField(
                label='Unité de produit',
                queryset=ProductUnit.objects.filter(
                    is_active=True).exclude(pk=1),
                required=False,
                widget=forms.Select(
                    attrs={'class': 'selectpicker form-control',
                           'data-live-search': 'true'})
            )
        self.fields['quantity'] = forms.IntegerField(
            label='Quantité de produit unitaire (g, cl ...)',
            min_value=0,
            required=False
        )
        self.fields['name'] = forms.CharField(
            label='Nom',
            max_length=254,
            required=False
        )
        self.fields['brand'] = forms.CharField(max_length=255,
                                               label='Marque')


    def clean(self):
        cleaned_data = super(ProductBaseCreateForm, self).clean()
        type = cleaned_data.get('type')
        product_unit = cleaned_data.get('product_unit')
        quantity = cleaned_data.get('quantity')
        if type == 'container':
            if product_unit is None:
                raise forms.ValidationError(
                    'Une unité de produit est exigée pour un conteneur'
                )
            if quantity is None:
                raise forms.ValidationError(
                    'Une quantité d\'unité de produit est exigée pour un conteneur'
                )


class ProductUnitCreateForm(forms.Form):
    def __init__(self, **kwargs):
        shop = kwargs.pop('shop')
        super(ProductUnitCreateForm, self).__init__(**kwargs)
        self.fields['name'] = forms.CharField(max_length=255,
                                              label='Nom')
        self.fields['unit'] = forms.ChoiceField(
            label='Unité de calcul',
            choices=(('CL', 'cl'), ('G', 'g')))
        self.fields['type'] = forms.ChoiceField(
            label='Catégorie de produit',
            choices=(('keg', 'fût'), ('liquor', 'alcool fort'),
                     ('syrup', 'sirop'), ('soft', 'soft'),
                     ('food', 'alimentaire'), ('meat', 'viande'),
                     ('cheese', 'fromage'), ('side', 'accompagnement')))
        if shop is None:
            self.fields['shop'] = forms.ModelChoiceField(
                label='Magasin',
                queryset=Shop.objects.all().exclude(pk=1)
            )


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = ProductBase
        fields = ['name', 'description', 'brand', 'type', 'quantity',
                  'product_unit']


class ProductUpdatePriceForm(forms.Form):
    is_manual = forms.BooleanField(
        label='Gestion manuelle du prix', required=False)
    manual_price = forms.DecimalField(label='Prix manuel',
                                      decimal_places=2,
                                      max_digits=9, min_value=0,
                                      required=False)


class ShopCreateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'description', 'color']


class ShopUpdateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['description', 'color']


class ProductListForm(forms.Form):
    def __init__(self, **kwargs):
        shop = kwargs.pop('shop')
        super(ProductListForm, self).__init__(**kwargs)
        if shop is None:
            self.fields['shop'] = forms.ModelChoiceField(
                label='Magasin',
                queryset=Shop.objects.all().exclude(pk=1),
                required=False
            )
        self.fields['search'] = forms.CharField(
            label='Recherche',
            max_length=255,
            required=False)
        self.fields['type'] = forms.ChoiceField(
            label='Type de produit',
            choices=(('container', 'Conteneur'),
                     ('single_product', 'Produit unitaire')),
            required=False)


class ShopContainerCaseForm(forms.Form):
    name = forms.CharField(
        label='Nom',
        max_length=254
    )
    pk = forms.IntegerField(
        label='Pk',
        widget=forms.HiddenInput(),
        required=False
    )
    percentage = forms.FloatField(
        label='percentage',
        widget=forms.HiddenInput(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        shop = kwargs.pop('shop')
        super(ShopContainerCaseForm, self).__init__(*args, **kwargs)
        q = ProductBase.objects.filter(shop=shop, type='container')
        q_ids = [o.id for o in q if (o.quantity_products_stock() != 0)]
        q = q.filter(id__in=q_ids)
        self.fields['base_container'] = ModelChoiceFieldContainerWithQuantity(
            label='Conteneur',
            queryset=q,
            widget=forms.Select(attrs={'class': 'selectpicker',
                                       'data-live-search': 'True'}),
            required=False)
        self.fields['is_sold'] = forms.BooleanField(
            label='Le fût changé était vide ?',
            initial=False,
            required=False)


class ModelChoiceFieldContainerWithQuantity(ModelChoiceField):
    """
    """

    def label_from_instance(self, obj):
        list_container = Container.objects.filter(
            product_base=obj, is_sold=False)
        quantity_in_stock = list_container.count()
        return obj.__str__() + ' (' + str(quantity_in_stock) + ')'













class ReplacementActiveKegForm(forms.Form):

    """
    Sont proposés les produits de base seulement (pour ne pas avoir à scroller s'il y a 20 fûts d'un produit ...)
    Seuls les produits de base dont l'unité concene un fût,
    pour les produits de base dont un fût est sous une tireuse : au moins 2 fûts dispo (un sous et un autre en stock)
    pour les autres au moins 1 fût dispo (en stock)
    """

    def __init__(self, *args, **kwargs):
        list_active_keg = kwargs.pop('list_active_keg')
        super(ReplacementActiveKegForm, self).__init__(*args, **kwargs)

        query = ProductBase.objects.filter(product_unit__type='keg')
        for keg_base in query:
            list_container_from_keg_base = Container.objects.filter(product_base=keg_base, is_sold=False)

            # Si un seul conteneur existe, on vérifie que ce n'est pas celui sous la tireuse
            if list_container_from_keg_base.count() == 1:
                for active_keg in list_active_keg:
                    if active_keg in list_container_from_keg_base:
                        query = query.exclude(pk=keg_base.pk)
            # Si aucun conteneur existe, le produit de base n'est pas proposé
            elif list_container_from_keg_base.count() == 0:
                query = query.exclude(pk=keg_base.pk)

        # Ajout du conteneur "vide" via la définition du ModelChoice
        self.fields['new_keg_product_base'] = ModelChoiceFieldWithQuantity(label='Nouveau fût', queryset=query,
                                                                           list_active_keg=list_active_keg,
                                                                           empty_label='Tireuse vide',
                                                                           required=False)
        self.fields['is_sold'] = forms.BooleanField(required=False, label='L\'ancien fût est vide')


class ModelChoiceFieldWithQuantity(ModelChoiceField):
    """
    Override d'un ModelChoiceField en ajoutant la quantité de conteneurs disponibles (sans celui sous la tireuse)
    dans le nom du produit de base
    """
    def __init__(self, **kwargs):
        self.list_active_keg = kwargs.pop('list_active_keg')
        super(ModelChoiceFieldWithQuantity, self).__init__(**kwargs)

    def label_from_instance(self, obj):
        list_container = Container.objects.filter(product_base=obj, is_sold=False)
        quantity_in_stock = list_container.count()
        for cont in self.list_active_keg:
            if cont in list_container:
                quantity_in_stock -= 1

        return obj.__str__() + ' (' + str(quantity_in_stock) + ')'


class PurchaseAubergeForm(forms.Form):

    # Client
    client_username = forms.CharField(label='Client', widget=forms.TextInput(attrs={'class': 'autocomplete_username'}),
                                      validators=[autocomplete_username_validator])

    def __init__(self, *args, **kwargs):

        # Initialisation des listes de produits
        container_meat_list = kwargs.pop('container_meat_list')
        container_cheese_list = kwargs.pop('container_cheese_list')
        container_side_list = kwargs.pop('container_side_list')
        single_product_available_list = kwargs.pop('single_product_available_list')
        self.request = kwargs.pop('request')
        super(PurchaseAubergeForm, self).__init__(*args, **kwargs)

        # Création des éléments de formulaire
        for (i, t) in enumerate(single_product_available_list):
            self.fields['field_single_product_%s' % i] = forms.IntegerField(required=True, min_value=0)
        for (i, t) in enumerate(container_meat_list):
            self.fields['field_container_meat_%s' % i] = forms.IntegerField(required=True, min_value=0)
        for (i, t) in enumerate(container_cheese_list):
            self.fields['field_container_cheese_%s' % i] = forms.IntegerField(required=True, min_value=0)
        for (i, t) in enumerate(container_side_list):
            self.fields['field_container_side_%s' % i] = forms.IntegerField(required=True, min_value=0)

    def single_product_avalaible_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_single_product_'):
                yield (self.fields[name].label, value)

    def container_meat_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_container_meat_'):
                yield (self.fields[name].label, value)

    def container_cheese_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_container_cheese_'):
                yield (self.fields[name].label, value)

    def container_side_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_container_side_'):
                yield (self.fields[name].label, value)

    def clean(self):

        try:
            # Vérification de la commande sans provision
            if float(self.request.POST.get('hidden_balance_after')) < 0:
                raise forms.ValidationError('Commande sans provision')
        except ValueError:
            raise forms.ValidationError('Erreur, veuillez recharger la page (F5 dans la barre d\'url)')

        return super(PurchaseAubergeForm, self).clean()


# C-Vis
class PurchaseCvisForm(forms.Form):

    # Client
    client_username = forms.CharField(label='Client', widget=forms.TextInput(attrs={'class': 'autocomplete_username'}),
                                      validators=[autocomplete_username_validator])

    def __init__(self, *args, **kwargs):

        # Initialisation des listes de produits
        # container_consumable_list = kwargs.pop('container_side_list')
        single_product_available_list = kwargs.pop('single_product_available_list')
        self.request = kwargs.pop('request')
        super(PurchaseCvisForm, self).__init__(*args, **kwargs)

        # Création des éléments de formulaire
        for (i, t) in enumerate(single_product_available_list):
            self.fields['field_single_product_%s' % i] = forms.IntegerField(required=True, min_value=0)
        # for (i, t) in enumerate(container_consumable_list):
        #     self.fields['field_container_consumable_%s' % i] = forms.IntegerField(required=True, min_value=0)

    def single_product_avalaible_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_single_product_'):
                yield (self.fields[name].label, value)

    # def container_consumable_answers(self):
    #     for name, value in self.cleaned_data.items():
    #         if name.startwith('field_container_side_'):
    #             yield (self.fields[name].label, value)

    def clean(self):

        try:
            # Vérification de la commande sans provision
            if float(self.request.POST.get('hidden_balance_after')) < 0:
                raise forms.ValidationError('Commande sans provision')
        except ValueError:
            raise forms.ValidationError('Erreur, veuillez recharger la page (F5 dans la barre d\'url)')

        return super(PurchaseCvisForm, self).clean()


# BB
class PurchaseBkarsForm(forms.Form):

    # Client
    client_username = forms.CharField(label='Client', widget=forms.TextInput(attrs={'class': 'autocomplete_username'}),
                                      validators=[autocomplete_username_validator])

    def __init__(self, *args, **kwargs):

        # Initialisation des listes de produits
        # container_consumable_list = kwargs.pop('container_side_list')
        single_product_available_list = kwargs.pop('single_product_available_list')
        self.request = kwargs.pop('request')
        super(PurchaseBkarsForm, self).__init__(*args, **kwargs)

        # Création des éléments de formulaire
        for (i, t) in enumerate(single_product_available_list):
            self.fields['field_single_product_%s' % i] = forms.IntegerField(required=True, min_value=0)
        # for (i, t) in enumerate(container_consumable_list):
        #     self.fields['field_container_consumable_%s' % i] = forms.IntegerField(required=True, min_value=0)

    def single_product_avalaible_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_single_product_'):
                yield (self.fields[name].label, value)

    # def container_consumable_answers(self):
    #     for name, value in self.cleaned_data.items():
    #         if name.startwith('field_container_side_'):
    #             yield (self.fields[name].label, value)

    def clean(self):

        try:
            # Vérification de la commande sans provision
            if float(self.request.POST.get('hidden_balance_after')) < 0:
                raise forms.ValidationError('Commande sans provision')
        except ValueError:
            raise forms.ValidationError('Erreur, veuillez recharger la page (F5 dans la barre d\'url)')

        return super(PurchaseBkarsForm, self).clean()


class PurchaseFoyerForm(forms.Form):

    def __init__(self, *args, **kwargs):

        # Initialisation des listes de produits
        active_keg_container_list = kwargs.pop('active_keg_container_list')
        single_product_available_list = kwargs.pop('single_product_available_list')
        shooter_available_list = kwargs.pop('shooter_available_list')
        container_soft_list = kwargs.pop('container_soft_list')
        container_syrup_list = kwargs.pop('container_syrup_list')
        container_liquor_list = kwargs.pop('container_liquor_list')

        self.request = kwargs.pop('request')
        super(PurchaseFoyerForm, self).__init__(*args, **kwargs)

        # Création des éléments de formulaire
        for (i, t) in enumerate(active_keg_container_list):
            self.fields['field_active_keg_container_%s' % i] = forms.IntegerField(required=True, min_value=0)
        for (i, t) in enumerate(single_product_available_list):
            self.fields['field_single_product_%s' % i] = forms.IntegerField(required=True, min_value=0,
                                                                            max_value=len(t[1]))
        for (i, t) in enumerate(shooter_available_list):
            self.fields['field_shooter_%s' % i] = forms.IntegerField(required=True, min_value=0,
                                                                            max_value=len(t[1]))
        for (i, t) in enumerate(container_soft_list):
            self.fields['field_container_soft_%s' % i] = forms.IntegerField(required=True, min_value=0)
        for (i, t) in enumerate(container_syrup_list):
            self.fields['field_container_syrup_%s' % i] = forms.IntegerField(required=True, min_value=0)
        for (i, t) in enumerate(container_liquor_list):
            self.fields['field_container_liquor_%s' % i] = forms.IntegerField(required=True, min_value=0)
            self.fields['field_container_entire_liquor_%s' % i] = forms.IntegerField(required=True, min_value=0)

    # Fonctions de récupérations des réponses en POST
    def active_keg_container_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_active_keg_container_'):
                yield (self.fields[name].label, value)

    def single_product_available_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_single_product_'):
                yield (self.fields[name].label, value)

    def shooter_available_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_shooter_'):
                yield (self.fields[name].label, value)

    def container_soft_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_container_soft_'):
                yield (self.fields[name].label, value)

    def container_syrup_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_container_syrup_'):
                yield (self.fields[name].label, value)

    def container_liquor_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_container_liquor_'):
                yield (self.fields[name].label, value)

    def container_entire_liquor_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_container_entire_liquor_'):
                yield (self.fields[name].label, value)

    def clean(self):
        try:
            # Vérification de la commande sans provision
            if float(self.request.POST.get('hidden_balance_after')) < 0:
                raise forms.ValidationError('Commande sans provision')
        except ValueError:
            raise forms.ValidationError('Erreur, veuillez recharger la page (F5 dans la barre d\'url)')

        return super(PurchaseFoyerForm, self).clean()


class DebitZifoysForm(forms.Form):

        # Client
    client_username = forms.CharField(label='Client', widget=forms.TextInput(attrs={'class': 'autocomplete_username'}),
                                      validators=[autocomplete_username_validator])

    def __init__(self, *args, **kwargs):

        # Initialisation des listes de produits
        active_keg_container_list = kwargs.pop('active_keg_container_list')
        single_product_available_list = kwargs.pop('single_product_available_list')
        shooter_available_list = kwargs.pop('shooter_available_list')
        container_soft_list = kwargs.pop('container_soft_list')
        container_syrup_list = kwargs.pop('container_syrup_list')
        container_liquor_list = kwargs.pop('container_liquor_list')

        self.request = kwargs.pop('request')
        super(DebitZifoysForm, self).__init__(*args, **kwargs)

        # Création des éléments de formulaire
        for (i, t) in enumerate(active_keg_container_list):
            self.fields['field_active_keg_container_%s' % i] = forms.IntegerField(required=True, min_value=0)
        for (i, t) in enumerate(single_product_available_list):
            self.fields['field_single_product_%s' % i] = forms.IntegerField(required=True, min_value=0,
                                                                            max_value=len(t[1]))
        for (i, t) in enumerate(shooter_available_list):
            self.fields['field_shooter_%s' % i] = forms.IntegerField(required=True, min_value=0,
                                                                            max_value=len(t[1]))
        for (i, t) in enumerate(container_soft_list):
            self.fields['field_container_soft_%s' % i] = forms.IntegerField(required=True, min_value=0)
        for (i, t) in enumerate(container_syrup_list):
            self.fields['field_container_syrup_%s' % i] = forms.IntegerField(required=True, min_value=0)
        for (i, t) in enumerate(container_liquor_list):
            self.fields['field_container_liquor_%s' % i] = forms.IntegerField(required=True, min_value=0)
            self.fields['field_container_entire_liquor_%s' % i] = forms.IntegerField(required=True, min_value=0)

    # Fonctions de récupérations des réponses en POST
    def active_keg_container_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_active_keg_container_'):
                yield (self.fields[name].label, value)

    def single_product_available_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_single_product_'):
                yield (self.fields[name].label, value)

    def shooter_available_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_shooter_'):
                yield (self.fields[name].label, value)

    def container_soft_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_container_soft_'):
                yield (self.fields[name].label, value)

    def container_syrup_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_container_syrup_'):
                yield (self.fields[name].label, value)

    def container_liquor_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_container_liquor_'):
                yield (self.fields[name].label, value)

    def container_entire_liquor_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startwith('field_container_entire_liquor_'):
                yield (self.fields[name].label, value)

    def clean(self):
        try:
            # Vérification de la commande sans provision
            if float(self.request.POST.get('hidden_balance_after')) < 0:
                raise forms.ValidationError('Commande sans provision')
        except ValueError:
            raise forms.ValidationError('Erreur, veuillez recharger la page (F5 dans la barre d\'url)')

        return super(DebitZifoysForm, self).clean()
