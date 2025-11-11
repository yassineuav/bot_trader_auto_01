from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("source", models.CharField(max_length=128)),
                ("url", models.URLField(unique=True)),
                ("published_at", models.DateTimeField()),
                ("title", models.CharField(max_length=512)),
                ("body", models.TextField()),
                ("tickers", models.JSONField(default=list)),
                ("raw_json", models.JSONField(default=dict)),
            ],
            options={"ordering": ["-published_at"]},
        ),
        migrations.CreateModel(
            name="Config",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(max_length=128, unique=True)),
                ("value_json", models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name="PatternSnapshot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("symbol", models.CharField(max_length=16)),
                ("window_days", models.IntegerField(default=28)),
                ("features_json", models.JSONField(default=dict)),
                ("verdict", models.CharField(max_length=8)),
                ("confidence_pct", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="RunLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.CharField(max_length=64)),
                ("message", models.CharField(max_length=512)),
                ("payload_json", models.JSONField(default=dict)),
                ("level", models.CharField(default="INFO", max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name="Signal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("source", models.CharField(choices=[("news", "News"), ("ml", "Machine Learning"), ("fallback_llm", "Fallback LLM")], max_length=32)),
                ("symbol", models.CharField(max_length=16)),
                ("direction", models.CharField(choices=[("call", "Call"), ("put", "Put")], max_length=8)),
                ("confidence_pct", models.IntegerField()),
                ("reason", models.TextField()),
                ("expires_at", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("alpaca_id", models.CharField(max_length=64, unique=True)),
                ("symbol", models.CharField(max_length=16)),
                ("type", models.CharField(max_length=16)),
                ("side", models.CharField(max_length=8)),
                ("qty", models.IntegerField()),
                ("limit_price", models.DecimalField(decimal_places=4, max_digits=12)),
                ("status", models.CharField(max_length=32)),
                ("filled_qty", models.IntegerField(default=0)),
                ("avg_fill_price", models.DecimalField(decimal_places=4, default=0, max_digits=12)),
                ("signal", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="orders", to="db.signal")),
            ],
        ),
        migrations.CreateModel(
            name="Position",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("symbol", models.CharField(max_length=16)),
                ("side", models.CharField(max_length=8)),
                ("qty", models.IntegerField()),
                ("avg_price", models.DecimalField(decimal_places=4, max_digits=12)),
                ("tp_pct", models.DecimalField(decimal_places=2, max_digits=5)),
                ("sl_pct", models.DecimalField(decimal_places=2, max_digits=5)),
                ("opened_at", models.DateTimeField()),
                ("closed_at", models.DateTimeField(blank=True, null=True)),
                ("pnl_pct", models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Sentiment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("pos_pct", models.IntegerField()),
                ("neg_pct", models.IntegerField()),
                ("label", models.CharField(max_length=16)),
                ("llm_version", models.CharField(max_length=64)),
                ("trend_bull_bear", models.CharField(max_length=16)),
                ("trend_strength_pct", models.IntegerField()),
                ("crowd_reaction_text", models.TextField()),
                ("article", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sentiments", to="db.article")),
            ],
        ),
    ]
