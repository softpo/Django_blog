# coding: utf-8

from django.shortcuts import render

from user.models import Permission


def check_permission(user, perm_name):
    '''检查用户是否具有该权限'''
    user_perm = Permission.objects.get(id=user.pid)
    need_perm = Permission.objects.get(name=perm_name)
    # 管理员的权限，最大的
    # 一般情况，这两个值，是相等
    print('-------------------------------',user_perm,need_perm)
    # 评论地方需要的权限是：user（2）------>新用户（2）
    return user_perm.perm >= need_perm.perm


def permit(perm_name):
    '''权限检查装饰器'''
    print('---------------------------------------permit')
    def wrap1(view_func):
        print('++++++++++++++++++++++++++++')
        def wrap2(request, *args, **kwargs):
            print()
            user = getattr(request, 'user', None)
            print('---------------------------------user: ',user)
            if user is not None:
                if check_permission(user, perm_name):
                    return view_func(request, *args, **kwargs)
            return render(request, 'blockers.html')
        return wrap2
    return wrap1
