import random
from faker import Faker
from data_objects.qualifications.skill.skill import Skill

class SkillData:

    faker = Faker()
    SKILL = [
        "Copywriting",
        "Content Creation",
        "G Suite",
        "Google Analytics",
        "JIRA",
        "Photoshop",
        "Python",
        "React Native",
        "Selenium",
        "SQL",
        "Search Engine Optimization (SEO)"
    ]

    @staticmethod
    def get_skill_details() -> Skill:
        return Skill(
            skill=random.choice(SkillData.SKILL),
            years_of_experience=str(SkillData.faker.random_int(min=0, max=40)),
            comments=SkillData.faker.sentence(nb_words=10)
        )