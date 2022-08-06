# Generated by Django 3.2.9 on 2022-08-06 16:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Favourited',
                'verbose_name_plural': 'Favourited',
                'ordering': ['-when_added'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Input ingredients name', max_length=250, verbose_name='Ingredient')),
                ('measurement_unit', models.CharField(help_text='Input measurement units', max_length=10, verbose_name='Measurement units')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IngredientInRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(null=True, verbose_name='Amount value of ingredient')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_amount', to='foodgram.ingredient', verbose_name='Ingredient in recipe')),
            ],
            options={
                'verbose_name': 'Ingredients amount in recipe',
                'verbose_name_plural': 'Ingredients amount in recipe',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Input recipes name', max_length=200, verbose_name='Name')),
                ('text', models.TextField(default='', help_text='How this thing should be cooked', verbose_name='Description')),
                ('cooking_time', models.PositiveSmallIntegerField(help_text='Input cooking time in minutes', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Cooking time')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Publication time')),
                ('image', models.ImageField(blank=True, help_text='Upload image', upload_to='recipes/media/', verbose_name='Image')),
                ('author', models.ForeignKey(help_text='This is the author of the recipe', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('ingredients', models.ManyToManyField(blank=True, help_text='Choose ingredients for your recipe', related_name='recipes', through='foodgram.IngredientInRecipe', to='foodgram.Ingredient', verbose_name='Ingredients')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Tags name', max_length=250, verbose_name='Tag')),
                ('color', models.CharField(default='#ffffff', help_text='Tags colour', max_length=7, verbose_name='HEX colour')),
                ('slug', models.SlugField(help_text='Tags slug', unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TagsInRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram.recipe')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodgram.tag', verbose_name='Тag in recipe')),
            ],
            options={
                'verbose_name': 'Tags in recipe',
                'verbose_name_plural': 'Tags in recipe',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when_added', models.DateTimeField(auto_now_add=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_in_shopping_cart', to='foodgram.recipe', verbose_name='Recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_in_shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Buying List',
                'verbose_name_plural': 'Buying List',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Choose recipes tags', related_name='recipes', through='foodgram.TagsInRecipe', to='foodgram.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='ingredientinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_amount', to='foodgram.recipe', verbose_name='Recipe'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ingredient'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='foodgram.recipe', verbose_name='Recipe'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_cart'),
        ),
        migrations.AddConstraint(
            model_name='ingredientinrecipe',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_amount'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite'),
        ),
    ]
