class MachineAccessMixin:
    """
    Ограничивает queryset машин по роли пользователя.
    Должен идти ПЕРЕД FilterView в наследовании.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        # Гости видят только через отдельный поиск (реализуем на след. шаге)
        if not user.is_authenticated:
            return qs.none()

        profile = getattr(user, 'profile', None)
        if not profile:
            return qs.none()

        role = profile.role
        org = profile.organization

        if role == 'manager':
            return qs.filter(is_deleted=False)
        elif role == 'client' and org:
            return qs.filter(client=org, is_deleted=False)
        elif role == 'service' and org:
            return qs.filter(service_company=org, is_deleted=False)

        return qs.none()