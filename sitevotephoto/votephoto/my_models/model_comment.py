from .model_photo import *


class Comment(models.Model):
    content = models.TextField(blank=False)
    dateCreate = models.DateField(auto_now_add=True)
    dateUpdate = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    Parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True)

    def get_absolute_url(self):
        return reverse('show_comment', kwargs={
            'commentID': self.pk
        })

    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.content
