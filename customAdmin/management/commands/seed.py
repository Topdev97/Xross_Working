from django.core.management.base import BaseCommand, CommandError
from customAdmin.models import *

PREFECTURES =  ['北海道','青森県','岩手県','宮城県','秋田県','山形県','福島県','茨城県','栃木県','群馬県','埼玉県','千葉県','東京都',
                '神奈川県','新潟県','富山県','石川県','福井県','山梨県','長野県', '岐阜県','静岡県','愛知県','三重県','滋賀県','京都府','大阪府',
                '兵庫県','奈良県','和歌山県','鳥取県','島根県','岡山県','広島県','山口県','徳島県','香川県','愛媛県','高知県','福岡県','佐賀県',
                '長崎県','熊本県','大分県','宮崎県','鹿児島県','沖縄県', '海外']

WORK_HOURS =  ['週1(20%)', '週2(40%)', '週3(60%)', '週4(80%)', '週5(100%)', '週5(100%)以上']
WORK_TYPES =  ['リモート', '常駐', '一部リモート(週1出勤)', '一部リモート(週2出勤)', '一部リモート(週3出勤)', '一部リモート(週4出勤)', '不定期']

CATEGROIES =  [
    {
        "name": 'システム開発',
        "skills": ["React", "Vue", "Next", "Nuxt", "Typescript", "Javascript", "Python", "Django", "PHP", "Laravel"]
    },
    {
        "name": 'アプリ・スマートフォン開発',
        "skills": ["ReactNative", "Android", "Java", "Kotlin", "Swift"]
    },
    {
        "name": 'ホームページ制作・Webデザイン',
        "skills": ["Figma", "HTML", "CSS", "Bootstrap", "Design", "AdobeXD"]
    },
    {
        "name": 'ECサイト・ネットショップ構築',
        "skills": ["EC-Cube", "Shopify", "MakeShop"]
    },
    {
        "name": 'デザイン',
        "skills": []
    },
    {
        "name": '動画・映像・アニメーション',
        "skills": []
    },
    {
        "name": '音楽・音響・ナレーション',
        "skills": []
    },
    {
        "name": 'ビジネス・マーケティング・企画',
        "skills": []
    },
    {
        "name": 'ライティング・記事作成',
        "skills": []
    },
    {
        "name": '事務・カンタン作業',
        "skills": []
    },
    {
        "name": '写真・画像',
        "skills": []
    },
    ]


class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options):
        self.initialize_prefectures()
        self.initialize_workhours()
        self.initialize_worktypes()
        self.initialize_categories()
        
        pass

    def initialize_prefectures(self):
        disp_order = 1
        Prefecture.objects.filter().delete()
        for prefecture in PREFECTURES:
            m_prefecture = Prefecture(name=prefecture, display_order=disp_order)
            m_prefecture.save()
            disp_order= disp_order+1

        
    def initialize_workhours(self):
        disp_order = 1
        WorkHour.objects.filter().delete()
        for workhour in WORK_HOURS:
            m_workhour = WorkHour(name=workhour, display_order=disp_order)
            m_workhour.save()
            disp_order= disp_order+1


    def initialize_worktypes(self):
        disp_order = 1
        WorkType.objects.filter().delete()
        for worktype in WORK_TYPES:
            m_worktype = WorkType(name=worktype, display_order=disp_order)
            m_worktype.save()
            disp_order= disp_order+1


    def initialize_categories(self):
        disp_order = 1
        Category.objects.filter().delete()
        for category in CATEGROIES:
            m_category = Category(name=category['name'], display_order=disp_order)
            m_category.save()

            for skill in category['skills']:
                m_skill = Skill(category=m_category, name=skill)
                m_skill.save()

            disp_order= disp_order+1
        