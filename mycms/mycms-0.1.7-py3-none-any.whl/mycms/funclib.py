from  faker import Faker
import random
def get_fake_contents(num_paragraphs):
    fake = Faker()
    
    paragraphs = []
    for c in range(num_paragraphs):
        num_sentences = random.randint(5,10)
        paragraphs.append(" ".join(fake.paragraphs(num_sentences)))
        
    return "\n\n".join(paragraphs)