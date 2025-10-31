from django.db import models

# Create your models here.

class Voter(models.Model):
    '''
    Store/represent the data from one potential voter from the city
    of Newton. Voter ID Number,Last Name,First Name,Residential Address
    - Street Number,Residential Address - Street Name,Residential Address 
    - Apartment Number,Residential Address - Zip Code,Date of Birth,Date of 
    Registration,Party Affiliation,Precinct Number,v20state,v21town,v21primary,
    v22general,v23town,voter_score
    '''
    voter_id_number = models.CharField()
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.CharField(blank=True)
    zip_code = models.IntegerField()
    DOB = models.DateField()
    date_of_registration = models.DateField()
    party = models.CharField(max_length=2)
    precinct_number = models.IntegerField()
    v20state = models.TextField()
    v21town= models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''

        return f'{self.first_name} {self.last_name} {self.DOB} {self.zip_code} {self.v22general} {self.voter_score}'
    

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    # Voter.objects.all().delete()
	
    filename = "/Users/sycds/OneDrive/Desktop/School/CS 412/Data/voter_analytics/newton_voters.csv"
    f = open(filename)
    f.readline() # remove headers
 

    for line in f:
        fields = line.split(',')
        
        try:
            # create a new instance of Voter object with this record from CSV
            voter = Voter(
                        voter_id_number=fields[0],
                        last_name=fields[1],
                        first_name=fields[2],
                        street_number=fields[3],
                        street_name=fields[4],
                        apartment_number=fields[5],
                        zip_code=fields[6],
                        DOB=fields[7],
                        date_of_registration=fields[8],
                        party=fields[9],
                        precinct_number=fields[10],
                        v20state=fields[11],
                        v21town=fields[12],
                        v21primary=fields[13],
                        v22general=fields[14],
                        v23town=fields[15],
                        voter_score=fields[16],
                        )
            
    
    
            voter.save() # commit to database
            print(f'Created result: {voter}')
                
        except Exception as e:
                print(f"Error : {e}")
                print(f"Skipped: {fields}")
        
        print(f'Done. Created {len(Voter.objects.all())} Voters.')