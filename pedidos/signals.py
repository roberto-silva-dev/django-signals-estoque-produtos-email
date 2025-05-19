from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.conf import settings
from django.core.mail import send_mail
from pedidos.models import Pedido


@receiver(post_save, sender=Pedido)
def atualizar_estoque(sender, instance, created, **kwargs):
    if created:
        produto = instance.produto
        produto.estoque -= instance.quantidade
        produto.save()
        print(f"Estoque atualizado para o produto {produto.nome}: {produto.estoque}")

        # Enviar e-mail após o commit da transação
        def notificar_por_email():
            print(f"Enviando e-mail ...")
            if send_mail(
                f'Novo pedido realizado | ID {instance.id}',
                f'Um novo pedido foi realizado:\n\nProduto: {produto.nome}\nQuantidade: {instance.quantidade}\nEstoque atual: {produto.estoque}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_PEDIDO_DESTINO],
                fail_silently=False,
            ):
                print('Email enviado para ', settings.EMAIL_PEDIDO_DESTINO)
        transaction.on_commit(notificar_por_email)
