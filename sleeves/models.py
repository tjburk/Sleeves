from django.db import models

class Album(models.Model):
    album = models.OneToOneField('Media', models.DO_NOTHING, primary_key=True)
    album_type = models.CharField(max_length=200, blank=True, null=True)
    album_art = models.CharField(max_length=200, blank=True, null=True)
    record_label = models.CharField(max_length=200, blank=True, null=True)
    artist = models.ForeignKey('Artist', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'album'


class AlbumHasGenre(models.Model):
    genre = models.ForeignKey('Genre', models.DO_NOTHING)
    album = models.OneToOneField('Media', models.DO_NOTHING, primary_key=True)  # The composite primary key (album_id, genre_id) found, that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = 'album_has_genre'
        unique_together = (('album', 'genre'),)


class Artist(models.Model):
    artist_id = models.CharField(primary_key=True, max_length=50)
    artist_name = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artist'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Episode(models.Model):
    episode = models.OneToOneField('Media', models.DO_NOTHING, primary_key=True)
    release_date = models.DateField(blank=True, null=True)
    synopsis = models.CharField(max_length=10000, blank=True, null=True)
    podcast = models.ForeignKey('Media', models.DO_NOTHING, related_name='episode_podcast_set', blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'episode'


class FilterMediaArtist(models.Model):
    id = models.BigAutoField(primary_key=True)
    artist_id = models.CharField(max_length=50)
    artist_name = models.CharField(max_length=200)
    bio = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'filter_media_artist'


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genre'


class Media(models.Model):
    spotify_id = models.CharField(primary_key=True, max_length=50)
    overall_rating = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media'


class Podcast(models.Model):
    podcast = models.OneToOneField(Media, models.DO_NOTHING, primary_key=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    producer = models.CharField(max_length=40, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'podcast'


class Review(models.Model):
    spotify = models.ForeignKey(Media, models.DO_NOTHING)
    title = models.CharField(max_length=40)
    star_rating = models.FloatField(blank=True, null=True)
    text = models.CharField(max_length=1000, blank=True, null=True)
    auth = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'


class Song(models.Model):
    song = models.OneToOneField(Media, models.DO_NOTHING, primary_key=True)
    tempo = models.IntegerField(blank=True, null=True)
    song_key = models.CharField(max_length=200, blank=True, null=True)
    loudness = models.IntegerField(blank=True, null=True)
    album_id = models.CharField(max_length=50, blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'song'