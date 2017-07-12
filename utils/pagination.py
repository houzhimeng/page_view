from django.shortcuts import HttpResponse,render,redirect
from django.utils.safestring import mark_safe

LIST = []
for i in range(159):
    LIST.append(i)

class Page:
    def __init__(self,current_page,data_count,per_page_count=10, pager_num=11):
        self.current_page = current_page
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.pager_num = pager_num

    @property
    def start(self):
        return (self.current_page-1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count


    @property
    def total_count(self):
        v, y = divmod(self.data_count, self.per_page_count)
        if y:
            v += 1
        return v

    def page_str(self,base_url):
        page_list = []

        if self.total_count < self.pager_num:
            start_index = 1
            end_index = self.total_count + 1
        else:
            if self.current_page <= (self.pager_num + 1) / 2:
                start_index = 1
                end_index = self.pager_num + 1
            else:
                start_index = self.current_page - (self.pager_num - 1) / 2
                end_index = self.current_page + (self.pager_num + 1) / 2

                if (self.current_page + (self.pager_num - 1) / 2) > self.total_count:
                    end_index = self.total_count + 1
                    start_index = self.total_count - self.pager_num + 1

        if self.current_page > 1:
            prev = '<a class="page" href="%s?p=%s">上一页</a>' % (base_url,self.current_page - 1)
            page_list.append(prev)

        for i in range(int(start_index), int(end_index)):                               ## 循环 1到 整个页数列表 +1
            if i == self.current_page:                                                  ## 假如 选择 第五页 ，那么其他页数不执行active 动作
                temp = '<a class="page active" href="%s?p=%s">%s</a>' % (base_url ,i ,i)
            else:
                temp = '<a class="page" href="%s?p=%s">%s</a>' % (base_url, i, i)
            page_list.append(temp)                                                      ## 每循环的数值加入到列表中

        if self.current_page < self.total_count:
            Next = '<a class="page" href="%s?p=%s">下一页</a>' % (base_url,self.current_page + 1)
            page_list.append(Next)

        page_str = "".join(page_list)  ## 拼接 下面页数
        page_str = mark_safe(page_str)  ## 安全转化信息

        return page_str


