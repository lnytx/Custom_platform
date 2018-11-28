# -*- coding:utf-8 -*-
'''
Created on 2017年12月29日

@author: ning.lin
'''
'''
分页工具，page_url是指每页上的url
如：http://127.0.0.1:8000/pag2/?p=1
此时page_url=pag2
'''
 
class Pagination(object):
    def __init__(self,current_page,total_page_count,per_page_item_num=10,max_page_num=7,page_url=None):
        # 当前页
        self.current_page = current_page
        try:
            v = int(current_page)
            if v <= 0:
                v = 1
            self.current_page = v
        except Exception as e:
            self.current_page = 1
        # 数据总个数
        self.total_page_count = total_page_count
        # 每一页显示的页面元素个数
        self.per_page_item_num = per_page_item_num
        # 最大显示页码
        self.max_page_num = max_page_num
        self.page_url = page_url

    def start_page_item(self):
        '''
        开始显示的页面元素，即从第几个页面链接开始显示
        :return: 当前页减一乘以每个页面最多显示元素个数
        '''
        return (self.current_page-1) * self.per_page_item_num

    def end_page_item(self):
        '''
        结束显示的页面元素，即最后一个页面元素的显示
        :return: 当前页乘以每个页面显示的最大元素个数
        '''
        return self.current_page * self.per_page_item_num

    # @property 是让num_pages变成以静态属性方式访问。
    @property
    def num_pages(self):
        '''
        总页码数量
        :return: 当b为零的时候代表是可整除的，a就是返回值，当不能整除时a+1返回。
        '''
        a,b = divmod(self.total_page_count,self.per_page_item_num)
        if b == 0:
            return a
        return a+1

    def page_num_range(self):
        '''
        页码的显示范围
        :return:
        '''

        # 判断如果页面总数量小于显示页面的总数量，那么返回最大的页面总数量。
        if self.num_pages < self.max_page_num:
            return range(1, self.max_page_num + 1)
        part = int(self.max_page_num / 2)

        # 判断当前页小于等于最大显示页的一半，那么返回1到最大显示页数量。
        if self.current_page <= part:
            return range(1, self.max_page_num + 1)

        # 当选择页数加上显示页数的一半的时候，说明越界了，例如最大也数是15，显示页数是10，我选择11页，那么11+5等于16，大于15，那么就显示总页数15-11+1，15+1
        if (self.current_page + part) > self.num_pages:
            # 那么返回总页数前去当前显示页数个数+1的值，和总页数+1的值。
            return range(self.num_pages - self.max_page_num + 1, self.num_pages + 1)

        # 当选择页大于当前总页数的一半的时候，返回当前选择页的前五个和后五个页数。
        return range(self.current_page - part, self.current_page + part + 1)

    def page_str(self):
        page_list=[]
        first = "<li><a href='/%s?p=1'>首页</a></li>" % (self.page_url,)
        page_list.append(first)

        if self.current_page == 1:
            prev = "<li><a href='#'>上一页</a></li>"
        else:
            prev = "<li><a href='/%s?p=%s'>上一页</a></li>" % (self.page_url,self.current_page - 1)
        page_list.append(prev)

        for i in self.page_num_range():
            if i == self.current_page:
                temp = "<li class='active'><a href='/%s?p=%s'>%s</a></li>" %(self.page_url,i,i)
            else:
                temp = "<li><a href='/%s?p=%s'>%s</a></li>" % (self.page_url,i, i)
            page_list.append(temp)

        if self.current_page == self.num_pages:
            nex = "<li><a href='#'>下一页</a></li>"
        else:
            nex = "<li><a href='/%s?p=%s'>下一页</a></li>" % (self.page_url,self.current_page + 1)
        page_list.append(nex)

        last = "<li><a href='/%s?p=%s'>尾页</a></li>" %(self.page_url,self.num_pages)
        page_list.append(last)

        return ''.join(page_list)
    def search_page_str(self):
        page_list=[]
        first = "<li><a href='/%s&p=1'>首页</a></li>" % (self.page_url,)
        page_list.append(first)

        if self.current_page == 1:
            prev = "<li><a href='#'>上一页</a></li>"
        else:
            prev = "<li><a href='/%s&p=%s'>上一页</a></li>" % (self.page_url,self.current_page - 1)
        page_list.append(prev)

        for i in self.page_num_range():
            if i == self.current_page:
                temp = "<li class='active'><a href='/%&?p=%s'>%s</a></li>" %(self.page_url,i,i)
            else:
                temp = "<li><a href='/%s&p=%s'>%s</a></li>" % (self.page_url,i, i)
            page_list.append(temp)

        if self.current_page == self.num_pages:
            nex = "<li><a href='#'>下一页</a></li>"
        else:
            nex = "<li><a href='/%s&p=%s'>下一页</a></li>" % (self.page_url,self.current_page + 1)
        page_list.append(nex)

        last = "<li><a href='/%s&p=%s'>尾页</a></li>" %(self.page_url,self.num_pages)
        page_list.append(last)

        return ''.join(page_list)