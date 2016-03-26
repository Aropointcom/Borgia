# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 16:51
from __future__ import unicode_literals

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('surname', models.CharField(blank=True, max_length=255, null=True)),
                ('family', models.CharField(blank=True, max_length=255, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('year', models.IntegerField(blank=True, choices=[(1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015)], null=True)),
                ('campus', models.CharField(blank=True, choices=[('ME', 'Me'), ('KA', 'Ka'), ('CH', 'Ch'), ('AI', 'Ai'), ('BO', 'Bo'), ('LI', 'Li'), ('CL', 'Cl'), ('KIN', 'Kin')], max_length=2, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('token_id', models.CharField(blank=True, max_length=6, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': (('presidents_group_manage', 'Gérer le groupe des présidents'), ('tresoriers_group_manage', 'Gérer le groupe des trésoriers'), ('chefs_gestionnaires_du_foyer_group_manage', 'Gérer le groupe des chefs gestionnaires du foyer'), ('gestionnaires_du_foyer_group_manage', 'Gérer le groupe des gestionnaires du foyer'), ('chefs_gestionnaires_de_l_auberge_group_manage', "Gérer le groupe des chefs gestionnaires de l'auberge"), ('gestionnaires_de_l_auberge_group_manage', "Gérer le groupe des gestionnaires de l'auberge"), ('gadz_arts_group_manage', "Gérer le groupe des Gadz'Arts"), ('membres_d_honneurs_group_manage', "Gérer le groupe des membres d'honneurs"), ('membres_speciaux_group_manage', 'Gérer le groupe des membres spéciaux'), ('vices_presidents_delegues_a_la_vie_interne_group_manage', 'Gérer le groupe des vices présidents délégués à la vie interne'), ('reach_workboard_treasury', 'Accéder au workboard de la trésorie'), ('reach_workboard_presidents', 'Accéder au workboard des présidents'), ('reach_workboard_vices_presidents_vie_interne', 'Accéder au workboard des vices présidents délégués à la vie interne'), ('list_user', 'Lister les users'), ('retrieve_user', 'Afficher les users'), ('supply_account', "Ajouter de l'argent à un compte"), ('link_token_user', 'Lier un jeton à un user'), ('add_product', 'Ajouter des produits')),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
