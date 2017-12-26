from extra_apps import xadmin
from .models import EmailVerifyRecord
from .models import Banner
from  xadmin import views


class EmailVerifyRecordAdmin():
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin():
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


class BaseSetting():
    '''
    增加主题样式
    '''
    enable_themes = True
    use_bootswatch = True


class GlobalSetting():
    '''
    修改全局配置
    '''
    site_title = "自学网后台管理系统"
    site_footer = "http://www.cnblogs.com/Jeffding/"
    menu_style = "accordion"


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)