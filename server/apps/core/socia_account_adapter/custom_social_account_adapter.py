from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        """
        自定义用户创建过程
        """
        user = super().populate_user(request, sociallogin, data)

        # 从微信获取的数据
        if sociallogin.account.provider == "weixin":
            # 使用微信用户信息设置用户属性
            extra_data = sociallogin.account.extra_data

            # 设置用户名（如果需要）
            openid = extra_data.get("openid", "")
            user.username = f"wx_{openid[:10]}"

            # 设置其他用户信息
            if "nickname" in extra_data:
                user.nickname = extra_data.get("nickname")

            # 如果需要设置邮箱
            if not user.email and "unionid" in extra_data:
                user.email = f"{extra_data.get('unionid')}@example.com"

        return user

    def save_user(self, request, sociallogin, form=None):
        """
        保存用户时的自定义处理
        """
        user = super().save_user(request, sociallogin, form)

        # 在用户保存后执行其他操作
        if sociallogin.account.provider == "weixin":
            # 例如添加用户到特定组、设置权限等
            pass

        return user
