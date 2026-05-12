class MachineAccessMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        # 1. Менеджер / Суперпользователь → видит всё
        if user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'manager'):
            return qs.filter(is_deleted=False)

        # 2. Авторизованный клиент / сервис → только свои машины
        if user.is_authenticated and hasattr(user, 'profile'):
            profile = user.profile
            if profile.role == 'client' and profile.organization:
                return qs.filter(client=profile.organization, is_deleted=False)
            if profile.role == 'service' and profile.organization:
                return qs.filter(service_company=profile.organization, is_deleted=False)

        # 3. Гость → только непроданные машины (каталог)
        return qs.filter(client__isnull=True, is_deleted=False)