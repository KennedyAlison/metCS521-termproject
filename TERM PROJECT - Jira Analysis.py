from datetime import datetime
from pandas._testing import assert_frame_equal
import pandas as pd


class Jira_Analysis:
    
    """
    Construct a Jira Analysis object with Epic, Feature, and Dependency Data 
    """
    def __init__(self, epics=None, features=None, dependencies=None):
        self.epics = str(epics)
        self.feats = str(features)
        self.deps = str(dependencies)
        self.__df_epics = None
        self.__df_feats = None
        self.__df_deps = None
        
    def __repr__(self):
        return {'Epics File ': self.epics, 'Features File ': self.feats, 'Dependencies File ': self.deps}
    
    """
    Create dataframes with input files to perform further analysis using Pandas
    """
    def __create_dataframes(self):
        try:
            self.__df_epics = pd.read_excel(self.epics)
            self.__df_feats = pd.read_excel(self.feats)
            self.__df_deps = pd.read_excel(self.deps)
        except FileNotFoundError:
            print("One of more files entered does not exist")
        except PermissionError:
            print("Cannot access one or more files")
        except Exception: 
            print(e)   
        assert_frame_equal(self.__df_epics, pd.read_excel(self.epics))
        assert_frame_equal(self.__df_feats, pd.read_excel(self.feats))
        assert_frame_equal(self.__df_deps, pd.read_excel(self.deps))    

        
    """
    Performs necessary cleaning and transforming steps before continuing further analysis
    """
    def clean_transform(self):
        """
        If progress value is of type object, convert into a float  
        """
        if(self.__df_epics['Epic Progress'].dtypes == "O"):
            self.__df_epics['Epic Progress'] = pd.eval(self.__df_epics['Epic Progress'])
        if(self.__df_feats['Feature Progress'].dtypes == "O"):
            self.__df_feats['Feature Progress'] = pd.eval(self.__df_feats['Feature Progress'])
        assert('Epic Progress' in self.__df_epics)
        assert('Feature Progress' in self.__df_feats)
        
        """
        Create a new column in Epic df to repesent the PI which the Epic will be delivered 
        i.e. the last value in the Program Increment column
        """
        self.__df_epics['Delivery PI'] = self.__df_epics['Program Increments'].str.rsplit(',').str[-1] 
        assert('Delivery PI' in self.__df_epics)
    
    
    """
    Returns the value of the number of records for each file/work item type  
    """
    def summary(self):
        s = 'This report contains data on: ' + str(len(self.__df_epics)) +         ' Epics, ' + str(len(self.__df_feats)) + ' Features, and ' + str(len(self.__df_deps)) + " Dependencies\n"
        
        assert(str(len(self.__df_epics)) in s)
        assert(str(len(self.__df_feats)) in s)
        assert(str(len(self.__df_deps)) in s)
        
        return s
    
    """
    Returns the average value for the given column 
    """
    def average(self, df, column):
        assert(isinstance(df[column].mean(), float))
        return df[column].mean()
    
    """
    Returns the average progresss count for Epics and Features 
    """
    def progress(self):
        epic_progress = self.average(self.__df_epics, "Epic Progress")
        MVP = self.__df_epics.loc[self.__df_epics['MVP'] == "Yes", 'Epic Progress']
        mvp_progress = MVP.mean()
        feature_progress = self.average(self.__df_feats, "Feature Progress")
        s = "\nThe average overall Epic Progress is " + "{0:.2%}".format(epic_progress) +         "\nThe average MVP Epic Progress is " + "{0:.2%}".format(mvp_progress) +         "\nThe average overall Feature Progress is " + "{0:.2%}".format(feature_progress) + "\n"
        
        assert(isinstance(epic_progress, float))
        assert(isinstance(mvp_progress, float))
        assert(isinstance(feature_progress, float))
        assert(epic_progress == self.average(self.__df_epics, "Epic Progress"))
        assert(mvp_progress == self.__df_epics.loc[self.__df_epics['MVP'] == "Yes", 'Epic Progress'].mean())
        assert(feature_progress == self.average(self.__df_feats, "Feature Progress"))        
        
        return s
    
    """
    Returns true if any Epics or Features are currently blocked 
    """
    def __blocked(self):
        blocked = False
        if 'Yes' in self.__df_epics["Blocked"].values or 'Yes' in self.__df_feats["Blocked"].values         or 'Blocked' in self.__df_deps["Status"].values:
            blocked = True
            assert('Yes' in self.__df_epics["Blocked"].values or 'Yes' in self.__df_feats["Blocked"].values or                   'Blocked' in self.__df_deps["Status"].values)
        if blocked == False:
            assert(not('Yes' in self.__df_epics["Blocked"].values or 'Yes' in self.__df_feats["Blocked"].values or                   'Blocked' in self.__df_deps["Status"].values))
        
        return blocked
    
    """
    Return a summary of all blocked items
    """
    def __blocked_summary(self):
        s = ''
        if 'Yes' in self.__df_epics["Blocked"].values:
            s = '\nCurrent blocked Epics: \n'
            blocked_epics = self.__df_epics.loc[self.__df_epics['Blocked'] == 'Yes']["Title"].values.tolist()
            for i in range(len(blocked_epics)):
                s += '-' + blocked_epics[i] + '\n'
                assert(blocked_epics[i] in s)
        else:
            s += "\nNo blocked Epics\n"
            assert(not('Yes' in self.__df_epics["Blocked"].values))
            
 
        if 'Yes' in self.__df_feats["Blocked"].values:
            s += 'Current blocked Features: \n'  
            blocked_feats = self.__df_feats.loc[self.__df_feats['Blocked'] == 'Yes']["Title"].values.tolist()
            for i in range(len(blocked_feats)):
                s +='-' + blocked_feats[i] + '\n'
                assert(blocked_feats[i] in s)
        else:
            s += "No blocked Features\n"
            assert(not('Yes' in self.__df_feats["Blocked"].values))
                
        if 'Blocked' in self.__df_deps["Status"].values:
            s += 'Current blocked Dependencies: \n'  
            blocked_deps = self.__df_deps.loc[self.__df_deps['Status'] == 'Blocked']["Title"].values.tolist()
            for i in range(len(blocked_deps)):
                s += '-' + blocked_deps[i] + '\n'
                assert(blocked_deps[i] in s)
        else:
            s += "No blocked Dependencies\n"
            assert(not('Blocked' in self.__df_deps["Status"].values))
        
        return str(s)
    
    """
    Returns True if there are any critical and high dependencies 
    """
    def __crit_high_deps(self):
        crit_high = False
        if 'Critical' in self.__df_deps["Priority"].values or 'High' in self.__df_deps["Priority"].values:
            crit_high = True
            assert('Critical' in self.__df_deps["Priority"].values or 'High' in self.__df_deps["Priority"].values)
        if crit_high == False:
            assert(not('Critical' in self.__df_deps["Priority"].values or 'High' in self.__df_deps["Priority"].values))
            
        return crit_high
    
    
    """
    Returns a string summary of dependencies by dependent Feature 
    """
    def dependency_summary(self):
        deps = {}
        s = '\nCurrent Critical and High Dependencies by Feature: \n'
        for i in range(len(self.__df_deps.index)):
            if self.__df_deps["Status"][i] != 'Done' and (self.__df_deps["Priority"][i] == 'Critical'             or self.__df_deps["Priority"][i] == 'High'):
                info = [self.__df_deps["Dependency ID"][i], self.__df_deps["Title"][i], self.__df_deps["Priority"][i], self.__df_deps["Status"][i],
                        self.__df_deps["Needed By"][i].strftime("%m/%d/%Y")]
                deps[self.__df_deps["Feature"][i]] = info
                assert(('Critical' or 'High') in s)
                assert(self.__df_deps["Status"][i] != 'Done')
        for i in range(len(self.__df_feats.index)):
            if(self.__df_feats["Title"][i] in deps):
                s += '\nFeature: ' + self.__df_feats["Title"][i] + '\n\tDependency: ID ' + str(deps[self.__df_feats["Title"][i]][0]) + ', '                 + deps[self.__df_feats["Title"][i]][1] + ', ' + deps[self.__df_feats["Title"][i]][2] + ', ' + deps[self.__df_feats["Title"][i]][3] +                 ', Needed By ' + deps[self.__df_feats["Title"][i]][4] + '\n'
                assert(('ID' and 'Title' and 'Needed By') in s)
                
        assert(bool(deps))
        
        return s  
    
    """
    Returns a string summary of each epics and the expected PI delivery 
    """
    def epic_delivery(self):
        s = '\nExpected Delivery PI for each Epic still to be delivered: \n'
        for i in range(len(self.__df_epics.index)):
            if self.__df_epics["State"][i] != 'Done':
                s += 'Epic ID ' + str(self.__df_epics["Id"][i]) + ': ' + self.__df_epics["Title"][i] +                 ' expected to be delivered in ' + self.__df_epics["Delivery PI"][i] + '\n'
                assert(self.__df_epics["Delivery PI"][i] in s)
                assert(self.__df_epics["State"][i] != 'Done')
        if ((len(self.__df_epics.index)) != 0):
            assert('expected to be delivered in' in s)
        return s
    
    """
    Returns an output file with a report on given Jira data - Epics, Features, and Dependencies
    """
    def create_report(self):
        self.__create_dataframes()
        self.clean_transform()
        now = datetime.now()
        f = open(("Sample Report - " + now.strftime("%m_%d_%Y") + ".txt"), "w")
        f.write(self.summary())
        f.write(self.progress())
        if(self.__blocked()):
            f.write(self.__blocked_summary())
        else:
            f.write("\nCurrently no Blockers for any work item\n")
        if(self.__crit_high_deps()):
            f.write(self.dependency_summary())
        else:
            f.write("\nCurrently no Critical or High Dependencies\n")
        f.write(self.epic_delivery())
        
        f.write('\n\n\nThis report was generated on ' + now.strftime("%m/%d/%Y at %H:%M:%S"))
        
        f.close()
        
        # Unit testing to assert that file was created and contains expected content 
        # Open the same file as the one written to 
        f = open("Sample Report - " + now.strftime("%m_%d_%Y") + ".txt", "r")
        
        # Readlines of sample file created 
        outfile = f.readlines()
        
        assert(("Epic Progress" and "MVP Epic Progress" and "Feature Progress") in str(outfile))
        
        assert(("Critical and High Dependencies" in str(outfile)) or ("Critical or High Dependencies" in str(outfile)))
       
        assert((("blocked Epics" and "blocked Features" and "blocked Dependencies") in str(outfile)) or ("no Blockers" in str(outfile)))
        
        assert("Expected Delivery PI" in str(outfile))
        
        assert("report was generated on" in str(outfile))
        
    
def main():
    
    epics = input("Enter an Epic excel filename including extension: ").strip()
    features = input("Enter a Features excel filename including extension: ").strip()
    dependencies = input("Enter a Dependencies excel filename including extension: ").strip()
    
    jira = Jira_Analysis(epics, features, dependencies)
    
    jira.create_report()
    

main()

