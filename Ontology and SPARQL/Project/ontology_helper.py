import pathlib

from owlready2 import *

from ontology_query_result import OntologyQueryResult
from data_source_helper import IDataSourceHelper
from result import IResult

# Ignore useless warnings
warnings.filterwarnings("ignore")

# set local path
onto_path.append(str(pathlib.Path(__file__).parent.resolve()) + "/res")


class OntologyHelper(IDataSourceHelper):

    def __init__(self):
        # Load the desired ontology using the file path
        self.ontology = get_ontology("ontology.owl").load(only_local=True)

        self.result = OntologyQueryResult()

    def get_result_confidence(self) -> float:
        """
        The method "get_result_confidence" returns an interpretation of the query result from the ontology. A negative
        number indicates that the given scenario is found to contain fake information. A positive number indicates that
        the given scenario is truthful. The number also indicates the confidence of the ontology. The closer the number
        is to 0, the less confident the ontology is about the given scenario.
        :return: interpretation of query result
        """

        total_instances_set = self.result.get_total()
        positive_instances_set = self.result.get_positive()
        if len(total_instances_set) == 0:
            return 0
        if len(positive_instances_set) == 0:
            return -1

        return ((len(positive_instances_set) / len(total_instances_set)) - 0.5) * 2

    def get_nl_explanation(self, positive) -> str:
        if self.result.is_empty():
            return "My own knowledge about the world did not help me to answer this statement."

        answer = "My reasoning was as follows: There is evidence that "
        if positive:
            evidence = self.result.positive_results
        elif not positive:
            evidence = self.result.negative_results

        for query in evidence:
            answer += query + ", "
        return answer

    def execute_queries(self, scenario) -> IResult:

        """
                Above we have the examples from the provided code. Below we have what we have done :)
                SPARQL variables start with a ? or $ and can match any node (resource or literal) in the RDF dataset.
                "a" is a type predicate ... instances in all the classes using the a (rdf:type) relationship...
                When a triple ends with a semicolon, the subject from this triple will implicitly complete the following pair to an entire triple. So for example ex:isCapitalOf ?y is short for ?x ex:isCapitalOf ?y.
                The + sign behind the subClassOf pattern is a "1 or more levels deep" operator

                <http://www.semanticweb.org/jiba/ontologies/2017/0/test#ma_pizza> 
                <http://www.semanticweb.org/jiba/ontologies/2017/0/test#price> ?p . }""))
        """

        if scenario == "Healthy people are happy":
            """                                                                                  
            Here I'm starting to write the queries for the scenario "Healthy people are happy"
            We need several queries :
                (+) 1) Happy people don't suffer from any disease               -done   
                (+) 2) Sad people have scurvy                                   -done
                (+) 3) People that are training are happy people                -done
                (+) 4) People that eat recipes that have vegetable are happy    -done
                (+) 5) People that eat food packed with protein are happy       -done
                (+) 6) People that have Corona are not happy                    -done
                (+) 7) Young people are happy                                   -done
            """
            happy_people_no_disease = list(default_world.sparql("""
                                       PREFIX ex: <http://www.semanticweb.org/raoulbrigola/ontologies/2022/8/untitled-ontology-10#>
                                       PREFIX ex1: <http://www.semanticweb.org/schon/ontologies/2022/8/IntelligentAgentsG4#>
                
                                       SELECT DISTINCT ?person
                                        WHERE {
                                            ?person a ex:Person
                                            ?person ex:isHappy "true".
                                            FILTER NOT EXISTS {
                                                ?person ex:afflictedWithDisease ?disease
                                            }
                                        }
                                        """))
            self.result.positive_results["Healthy people are happy"] = happy_people_no_disease

            sad_with_scurvy = list(default_world.sparql("""
                               PREFIX ex: <http://www.semanticweb.org/raoulbrigola/ontologies/2022/8/untitled-ontology-10#>
                               PREFIX ex1: <http://www.semanticweb.org/schon/ontologies/2022/8/IntelligentAgentsG4#>
    
                               SELECT DISTINCT ?person
                                WHERE {
                                    ?person a ex:Person;
                                            ex:isHappy ?value;
                                            ex:afflictedWithDisease ?disease.
                                    ?disease a ex:Scurvy.
                                    FILTER (?value = "false")
                                }
                                """))
            self.result.positive_results["Sad people have scurvy"] = sad_with_scurvy

            happy_training_people = list(default_world.sparql("""
                                   PREFIX ex: <http://www.semanticweb.org/raoulbrigola/ontologies/2022/8/untitled-ontology-10#>
                                   PREFIX ex1: <http://www.semanticweb.org/schon/ontologies/2022/8/IntelligentAgentsG4#>
    
                                   SELECT DISTINCT ?person
                                    WHERE {
                                        ?person a ex:Person;
                                                ex:isHappy ?value;
                                                ex:plays ?sport.
                                        FILTER (?value = "true")
                                    }
                                    """))
            self.result.positive_results["People that are training are happy people"] = happy_training_people

            happy_vegetables_people = list(default_world.sparql("""
                                       PREFIX ex: <http://www.semanticweb.org/raoulbrigola/ontologies/2022/8/untitled-ontology-10#>
                                       PREFIX ex1: <http://www.semanticweb.org/schon/ontologies/2022/8/IntelligentAgentsG4#>
                
                                       SELECT DISTINCT ?person
                                       WHERE {
                                            ?person a ex:Person;
                                                    ex:isHappy "true";
                                                    ex:oftenEats ?things.
                                            ?things ex1:hasIngredient ?v.
                                            ?v a/rdfs:subClassOf ex1:Vegetables.
                                        }
                                        """))
            self.result.positive_results["People that eat recipes that have vegetable are happy"] = happy_vegetables_people

            happy_protein_people = list(default_world.sparql("""
                                   PREFIX ex: <http://www.semanticweb.org/raoulbrigola/ontologies/2022/8/untitled-ontology-10#>
                                   PREFIX ex1: <http://www.semanticweb.org/schon/ontologies/2022/8/IntelligentAgentsG4#>
    
                                   SELECT DISTINCT ?person
                                    WHERE {
                                        ?person a ex:Person;
                                                ex:isHappy "true";
                                                ex:oftenEats ?food.
                                        ?food ex1:hasIngredient ?i.
                                        ?i ex1:denseIn ?p.
                                        ?p a/rdfs:subClassOf* ex1:Protein.
                                    }
                                    """))
            self.result.positive_results["People that eat food packed with protein are happy"] = happy_protein_people

            sad_with_corona = list(default_world.sparql("""
                                   PREFIX ex: <http://www.semanticweb.org/raoulbrigola/ontologies/2022/8/untitled-ontology-10#>
                                   PREFIX ex1: <http://www.semanticweb.org/schon/ontologies/2022/8/IntelligentAgentsG4#>
    
                                   SELECT DISTINCT ?person
                                    WHERE {
                                        ?person a ex:Person;
                                                ex:isHappy ?value;
                                                ex:afflictedWithDisease ?disease.
                                        ?disease a ex:Corona.
                                        FILTER (?value = "false")
                                    }
                                    """))
            self.result.positive_results["People that have Corona are not happy"] = sad_with_corona

            young_people = list(default_world.sparql("""
                               PREFIX ex: <http://www.semanticweb.org/raoulbrigola/ontologies/2022/8/untitled-ontology-10#>
    
                               SELECT DISTINCT ?person
                                WHERE {
                                    ?person a ex:Person;
                                            ex:isHappy ?value;
                                            ex:hasAge ?age
                                    FILTER (?value = "true" && ?age<27)
                                }
                                """))
            self.result.positive_results["Young people are happy"] = young_people

        if scenario == "Individual sports require lower body":
            """
            Here I'm starting to write the queries for the scenario ``Individual sports require lower body"
            We need several queries :
                (+) 1) Individual sports that require lower body -done
                (-) 2) Individual sports that require upper body -done
            """

            individual_lower = list(default_world.sparql("""
                                   PREFIX ex: <http://www.semanticweb.org/raoulbrigola/ontologies/2022/8/untitled-ontology-10#>
                                   PREFIX ex1: <http://www.semanticweb.org/schon/ontologies/2022/8/IntelligentAgentsG4#>
        
                                   SELECT DISTINCT ?sport               
                                    WHERE{
                                        ?sport a/rdfs:subClassOf ex:Individual.
                                        ?sport ex:prominentlyRequires ?bodypart .
                                        ?bodypart a/rdfs:subClassOf ex:LowerBody.
                                    }
                                    """))
            self.result.positive_results["Individual sports require lower body"] = individual_lower

            individual_upper = list(default_world.sparql("""
                                       PREFIX ex: <http://www.semanticweb.org/raoulbrigola/ontologies/2022/8/untitled-ontology-10#>
                                       PREFIX ex1: <http://www.semanticweb.org/schon/ontologies/2022/8/IntelligentAgentsG4#>
    
                                       SELECT DISTINCT ?sport               
                                        WHERE{
                                            ?sport a/rdfs:subClassOf ex:Individual.
                                            ?sport ex:prominentlyRequires ?bodypart .
                                            ?bodypart a/rdfs:subClassOf ex:UpperBody.
                                        }
                                        """))
            self.result.negative_results["Individual sports require upper body"] = individual_upper

        if scenario == "Sugar is good for people":
            """
            Here I'm starting to write the queries for the scenario ``Sugar is good for people"
            We need several queries :
                (-) 1) Sugar causes diabetes                            -done
                (+) 2) People that eat sugar are happy                  -done
                (+) 3) People that eat sugar play sports                -done
                (-) 4) People that eat sugar have high blood pressure   -done
            """

            sugar_diabetes = list(default_world.sparql("""
                           PREFIX ex: <http://www.semanticweb.org/raoulbrigola/ontologies/2022/8/untitled-ontology-10#>
                           PREFIX ex1: <http://www.semanticweb.org/schon/ontologies/2022/8/IntelligentAgentsG4#>
    
                           SELECT DISTINCT ?s                          
                            WHERE{
                                ?s a ex1:Sugars.
                                ?s ex:causesDisease ?disease.
                                ?disease a/rdfs:subClassOf* ex:Diabetes.
                            }
                            """))
            self.result.negative_results["Sugar causes diabetes"] = sugar_diabetes

            sugar_happy_people = list(default_world.sparql("""
                                   PREFIX ex: <http://www.semanticweb.org/raoulbrigola/ontologies/2022/8/untitled-ontology-10#>
                                   PREFIX ex1: <http://www.semanticweb.org/schon/ontologies/2022/8/IntelligentAgentsG4#>
    
                                   SELECT DISTINCT ?person
                                   WHERE{
                                        ?person a ex:Person;
                                                ex:isHappy "true";
                                                ex:oftenEats ?recipe.
                                        ?recipe ex1:hasIngredient ?food.
                                        ?food ex1:denseIn ?s.
                                        ?s a/rdfs:subClassOf* ex1:Sugars.
                                        }
                                    """))
            self.result.positive_results["People that eat sugar are happy"] = sugar_happy_people

            sugar_sport_people = list(default_world.sparql("""
                                   PREFIX ex: <http://www.semanticweb.org/raoulbrigola/ontologies/2022/8/untitled-ontology-10#>
                                   PREFIX ex1: <http://www.semanticweb.org/schon/ontologies/2022/8/IntelligentAgentsG4#>
        
                                   SELECT DISTINCT ?person
                                   WHERE{
                                        ?person a ex:Person;
                                                ex:plays ?sport;
                                                ex:oftenEats ?recipe.
                                        ?recipe ex1:hasIngredient ?food.
                                        ?food ex1:denseIn ?s.
                                        ?s a/rdfs:subClassOf* ex1:Sugars.
                                        }
                                    """))
            self.result.positive_results["People that eat sugar play sports"] = sugar_sport_people

            sugar_HBP_people = list(default_world.sparql("""
                               PREFIX ex: <http://www.semanticweb.org/raoulbrigola/ontologies/2022/8/untitled-ontology-10#>
                               PREFIX ex1: <http://www.semanticweb.org/schon/ontologies/2022/8/IntelligentAgentsG4#>
    
                               SELECT DISTINCT ?person
                               WHERE{
                                    ?person a ex:Person;
                                            ex:afflictedWithCondition ?d;
                                            ex:oftenEats ?recipe.
                                    ?recipe ex1:hasIngredient ?food.
                                    ?food ex1:denseIn ?s.
                                    ?s a/rdfs:subClassOf* ex1:Sugars.
                                    ?d a/rdfs:subClassOf* ex:BloodPressure.
                                    FILTER (?d != "LowBlooPress")
                                    }
                                """))
            self.result.negative_results["People that eat sugar have high blood pressure"] = sugar_HBP_people

        return self.result
