
#  *** Assignment #9: Build a Social Network ***


class Person:
    '''
    A class representing a person in a social network.
    Attributes:
        name (str): The name of the person.
        friends (list): A list of friends (Person objects).
    Methods:
        add_friend(friend): Adds a friend to the person's friend list.
   '''
    def __init__(self, name: str):
        self.name = name
        self.friends = []

    def add_friend(self, friend: "Person") -> None:
        """Add a friend if not already present and not self."""
        if friend is self:
            return  # ignore self-friendship silently
        if friend not in self.friends:
            self.friends.append(friend)

    def __repr__(self):
        return f"Person({self.name!r})"
    
    


class SocialNetwork:
    '''
    A class representing a social network.
    Attributes:
        people (dict): A dictionary mapping names to Person objects.
    Methods:
        add_person(name): Adds a new person to the network.
        add_friendship(person1_name, person2_name): Creates a friendship between two people.
        print_network(): Prints the names of all people and their friends.
    '''
    
    def __init__(self):
        # key: person name (str), value: Person instance
        self.people: dict[str, Person] = {}

    def add_person(self, name: str) -> None:
        """Create and register a new person. Warn on duplicates."""
        if name in self.people:
            print(f"Person '{name}' already exists. Skipping duplicate.")
            return
        self.people[name] = Person(name)

    def add_friendship(self, person1_name: str, person2_name: str) -> None:
        """
        Prints helpful errors for missing nodes and self-friend attempts.
        """
        if person1_name == person2_name:
            print("Friendship not created. Cannot friend yourself.")
            return

        p1 = self.people.get(person1_name)
        p2 = self.people.get(person2_name)

        missing = [n for n, p in [(person1_name, p1), (person2_name, p2)] if p is None]
        if missing:
            print(f"Friendship not created. {' & '.join(missing)} "
                  f"{'does' if len(missing)==1 else 'do'} not exist!")
            return

        # Add both directions (undirected)
        before_len_p1 = len(p1.friends)
        before_len_p2 = len(p2.friends)
        p1.add_friend(p2)
        p2.add_friend(p1)

        # Optional info message on duplicates
        if len(p1.friends) == before_len_p1 and len(p2.friends) == before_len_p2:
            print(f"Friendship between '{person1_name}' and '{person2_name}' already exists.")


    def print_network(self) -> None:
        """
        Print each person and their friends in a certain order.
        Format:
        Alex is friends with: Jordan, Morgan, Taylor
        """
        # Sort names for readable output
        for name in sorted(self.people.keys()):
            person = self.people[name]
            friend_names = [f.name for f in person.friends]
            # Sort friend names alphabetically
            friend_names.sort()
            friends_str = ", ".join(friend_names) if friend_names else "(no friends)"
            print(f"{person.name} is friends with: {friends_str}")


    

# Test your code here
if __name__ == "__main__":
    network = SocialNetwork()

    # Add at least 6 people
    for n in ["Alex", "Jordan", "Morgan", "Taylor", "Casey", "Riley"]:
        network.add_person(n)

    # Edge case: duplicate person
    network.add_person("Alex")  # should warn and skip

    # Create at least 8 friendships
    network.add_friendship("Alex", "Jordan")
    network.add_friendship("Alex", "Morgan")
    network.add_friendship("Jordan", "Taylor")
    network.add_friendship("Morgan", "Casey")
    network.add_friendship("Taylor", "Riley")
    network.add_friendship("Casey", "Riley")
    network.add_friendship("Morgan", "Riley")
    network.add_friendship("Alex", "Taylor")

    # Edge cases
    network.add_friendship("Jordan", "Johnny")  # Johnny doesn't exist
    network.add_friendship("Alex", "Alex")      # self-friendship
    network.add_friendship("Alex", "Jordan")    # duplicate friendship

    # Print the network
    network.print_network()


    """
DESIGN MEMO

I chose a graph to model the social network because it matches how friendships work in real life.
Each person is a “node,” and each friendship is a “connection” between two people. People can
have many friends, and those friends can also be connected to each other in lots of different ways.
A graph makes this easy to show and update.

A simple list wouldn't work well, because a list can hold people but doesn't naturally show who is
friends with who. We would need extra steps or a lot of searching to find connections. A tree
also isn't a good fit. Trees have a parent-child shape and don't allow natural loops. But real
social networks have loops all the time (for example, Alex <-> Jordan <-> Taylor <-> Alex).

In my code, I keep a dictionary of people, and each person stores a list of their friends.
To add a new person I just add their name to the dictionary if it isn't already there.
Making a friendship means adding each person to the other's friend list, so the connection goes
both ways. I also include small checks to avoid adding the same friendship twice or letting someone
friend themselves by mistake.

When printing the network, I sort names so the output is predictable and easy to read. This can take
a little extra time with bigger lists, but it makes the results clearer. Overall, the graph structure
is simple to understand, grows well as we add more people and friendships, and fits the real-world
idea of a social network.
"""