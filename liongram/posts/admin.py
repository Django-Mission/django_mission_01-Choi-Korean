from django.contrib import admin
from .models import Post, Comment    # Post의 같은 경로상에 있기에, .(현재위치)으로 경로 지정 가능

# Register your models here.

# admin.site.register(Post)   # admin 페이지에 Post, Comment 클래스 등록. 와 개편하네;;

class CommentInline(admin.TabularInline):       # 댓글 전달할 클래스 만들기. StackedInline으로 하면 구분 부분이 매 값마다 세로로 나옴. Tabular는 가로로. 그때그때 편한거 쓰면됨
    model = Comment
    extra = 5       # 댓글추가 빈공란 개수(기본값)
    min_num = 3     # 위 비공란의 최소 개수( 이 이하로 삭제 불가)
    max_num = 5     # 마찬가지로 최대 개수. 이 이상으로 생성 불가
    verbose_name = '댓글'
    verbose_name_plural = '댓글'    # comment 부분 칸 이름 설정 속성


# 근데 커스터마이징 하려면 이렇게 상속받아서 해야함
@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'image', 'created_at', 'view_count', 'writer')    # list_display에 속성명(modes.Post에 설정해놓은) 넣으면 list_display에 추가됨.
    #list_display같은 속성명(변수명)은 공식문서에서 찾아서 써야됨

    # content 필드가 수정가능한 칸으로 변경됨
    # list_editable = ('content', ) #튜플로 쓸때 변수가 한개면 , 꼭 넣어줘야 됨 콤마

    list_filter = ('created_at', )
    search_fields = ('id', 'writer__username')
    search_help_text = '게시판 번호, 작성자 검색이 가능합니다.' 
    readonly_fields = ('created_at', )      # 작성일은 수정불가 데이터여서 안나오는데, readonly_fields로 넣어주면 확인 가능
    inlines = [CommentInline]       # 신기하네;; 걍 댓글 받고 자동으로 id 검색해서 글마다 댓글 넣어주는 건가
    actions = ['make_published']    # admin에 선택한 게시글 모두 지우기 같은 특수기능 추가. 이런 기능은 함수 직접 만들어서 넣어주면 됨

    def make_published(modeladmin, request, queryset):      # queryset은 페이지에서 전송한 데이터가 들어옴. 데이터 세개 선택/전송했으면 세개를 한셋으로
        for item in queryset:
            item.content= '규정 위반으로 글삭제'
            item.save()


# admin.site.register(Comment)

