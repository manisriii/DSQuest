from .. import LOG
from ..models.problems import Problem
import json


class AddProblems:
    def __init__(self, db):
        self.db = db

    def run(self):
        self.create_users()
        self.add_sqlproblems()
        try:
            self.db.session.commit()
        except Exception as e:
            LOG.error(e)

    def create_users(self):
        user1 = Problem(Id=1,
                        title="Create a DataFrame from List",
                        difficulty="Easy",
                        description="Write a solution to create a DataFrame from a 2D list called student_data. This "
                                    "2D list contains the IDs and ages of some students. The DataFrame should have "
                                    "two columns, student_id and age, and be in the same order as the original 2D "
                                    "list.",
                        example_input="student_data = [[1, 15], [2, 11], [3, 11], [4, 20]]",
                        example_output='+------------+-----+\n| student_id | age |\n+------------+-----+\n| 1         '
                                       ' | 15  |\n| 2          | 11  |\n| 3          | 11  |\n| 4          | 20  '
                                       '|\n+------------+-----+',
                        explanation='A DataFrame was created on top of student_data, with two columns named '
                                    'student_id and age.',
                        type='pandas',
                        solution_='''import pandas as pd
from typing import List

def createDataframe(student_data: List[List[int]]) -> pd.DataFrame:
    # Create DataFrame with specified column names
    df = pd.DataFrame(student_data, columns=["student_id", "age"])
    return df''',
                        test_cases=json.dumps([
                            {
                                "input": "student_data = [[1, 15], [2, 11], [3, 11], [4, 20]]",
                                "expected_output": {
                                    "headers": ["student_id", "age"],
                                    "values": [[1, 15], [2, 11], [3, 11], [4, 20]]
                                }
                            },
                            {
                                "input": "student_data = [[5, 25], [6, 30]]",
                                "expected_output": {
                                    "headers": ["student_id", "age"],
                                    "values": [[5, 25], [6, 30]]
                                }
                            },
                            {
                                "input": "student_data = [[7, 40]]",
                                "expected_output": {
                                    "headers": ["student_id", "age"],
                                    "values": [[7, 40]]
                                }
                            }
                        ]),
                        function_signature="import pandas as pd\nfrom typing import List\n\ndef createDataframe(student_data: List[List[int]]) -> pd.DataFrame:")
        self.db.session.merge(user1)
        user1 = Problem(Id=2,
                        title="Count a Number of Columns in a DataFram",
                        difficulty="Easy",
                        description="Write a solution to create a DataFrame from a 2D list called student_data. This "
                                    "2D list contains the IDs and ages of some students. The DataFrame should have "
                                    "two columns, student_id and age, and be in the same order as the original 2D "
                                    "list.",
                        example_input="student_data = [[1, 15], [2, 11], [3, 11], [4, 20]]",
                        example_output='+------------+-----+\n| student_id | age |\n+------------+-----+\n| 1         '
                                       ' | 15  |\n| 2          | 11  |\n| 3          | 11  |\n| 4          | 20  '
                                       '|\n+------------+-----+',
                        explanation='A DataFrame was created on top of student_data, with two columns named '
                                    'student_id and age.',
                        type='pandas',solution_='''import pandas as pd
from typing import List, Tuple

def createDataframe(student_data: List[List[int]]) -> Tuple[pd.DataFrame, int]:
    # Create DataFrame with specified column names
    df = pd.DataFrame(student_data, columns=["student_id", "age"])
    
    # Get the number of columns
    num_columns = df.shape[1]
    
    # Return both the DataFrame and the number of columns
    return num_columns''',
                        test_cases=json.dumps([
                            {
                                "input": "student_data = [[1, 15], [2, 11], [3, 11], [4, 20]]",
                                "expected_output": 2
                            },
                            {
                                "input": "student_data = [[5, 25], [6, 30]]",
                                "expected_output": 2
                            },
                            {
                                "input": "student_data = [[7, 40]]",
                                "expected_output": 2
                            }
                        ]),
                        function_signature="import pandas as pd\nfrom typing import List\n\ndef createDataframe(student_data: List[List[int]]) -> pd.DataFrame:")
        self.db.session.merge(user1)
        python_ = Problem(Id=3,
                          title="Two Sum",
                          difficulty="Easy",
                          description="Given an array of integers nums and an integer target, return indices of the "
                                      "two "
                                      "numbers such that they add up to target.You may assume that each input would "
                                      "have exactly one solution, and you may not use the same element twice.You can "
                                      "return the answer in any order.",
                          example_input="nums = [2,7,11,15], target = 9",
                          example_output='[0,1]',
                          explanation='Because nums[0] + nums[1] == 9, we return [0, 1].',
                          type='python',solution_='''def twoSum(nums, target):
        num_dict = {}
        for index, num in enumerate(nums):
            complement = target - num
            
            if complement in num_dict:
                return [num_dict[complement], index]
            
            num_dict[num] = index
        
        return []''',
                          test_cases=json.dumps([
                              {
                                  "input": {"nums": [2, 7, 11, 15], "target": 9},
                                  "expected_output": [0, 1]
                              },
                              {
                                  "input": {"nums": [3, 2, 4], "target": 6},
                                  "expected_output": [1, 2]
                              },
                              {
                                  "input": {"nums": [3, 3], "target": 6},
                                  "expected_output": [0, 1]
                              }
                          ]),
                          function_signature="def twoSum(nums: List[int], target: int) -> List[int]:")
        self.db.session.merge(python_)
        python_ = Problem(Id=4,
                          title="Longest Substring Without Repeating Characters",
                          difficulty="Medium",
                          description="Given a string s, find the length of the longest substring without repeating characters.",
                          example_input='s = "abcabcbb"',
                          example_output='3',
                          explanation='The answer is "abc", with the length of 3.',
                          type='python',solution_='''def lengthOfLongestSubstring(s: str) -> int:
        n = len(s)
        maxLength = 0
        charSet = set()
        left = 0
        
        for right in range(n):
            if s[right] not in charSet:
                charSet.add(s[right])
                maxLength = max(maxLength, right - left + 1)
            else:
                while s[right] in charSet:
                    charSet.remove(s[left])
                    left += 1
                charSet.add(s[right])
        
        return maxLength''',
                          test_cases=json.dumps([
                              {
                                  "input": "s='abcabcbb'",
                                  "expected_output": 3
                              },
                              {
                                  "input": "s='bbbbb'",
                                  "expected_output": 1
                              },
                              {
                                  "input": 's="pwwkew"',
                                  "expected_output": 3
                              }
                          ]),
                          function_signature="def lengthOfLongestSubstring(self, s: str) -> int:")
        self.db.session.merge(python_)
        python_ = Problem(Id=5,
                          title="Median of Two Sorted Arrays",
                          difficulty="Medium",
                          description="Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.The overall run time complexity should be O(log (m+n)).",
                          example_input='nums1 = [1,3], nums2 = [2]',
                          example_output='2.00000',
                          explanation='merged array = [1,2,3] and median is 2.',
                          type='python',solution_='''def findMedianSortedArrays(nums1,nums2):
    # Merge the arrays into a single sorted array.
    merged = nums1 + nums2

    # Sort the merged array.
    merged.sort()

    # Calculate the total number of elements in the merged array.
    total = len(merged)

    if total % 2 == 1:
        # If the total number of elements is odd, return the middle element as the median.
        return float(merged[total // 2])
    else:
        # If the total number of elements is even, calculate the average of the two middle elements as the median.
        middle1 = merged[total // 2 - 1]
        middle2 = merged[total // 2]
        return (float(middle1) + float(middle2)) / 2.0''',
                          test_cases=json.dumps([
                              {
                                  "input": {"nums1": [1, 3], "nums2": [2]},
                                  "expected_output": 2.00000
                              },
                              {
                                  "input": {"nums1": [1, 2], "nums2": [3, 4]},
                                  "expected_output": 2.50000
                              },
                              {
                                  "input": {"nums1": [1, 3], "nums2": [2]},
                                  "expected_output": 2.50000
                              }
                          ]),
                          function_signature="def findMedianSortedArrays(nums1, nums2):")
        self.db.session.merge(python_)
        python_ = Problem(Id=6,
                          title="Longest Palindromic Substring",
                          difficulty="Medium",
                          description="Given a string s, return the longest palindromic substring in s.",
                          example_input='s = "babad"',
                          example_output="bab",
                          explanation='"aba" is also a valid answer.',
                          type='python',solution_='''def longestPalindrome(s: str) -> str:
    if len(s) <= 1:
        return s

    def expand_from_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    max_str = s[0]

    for i in range(len(s) - 1):
        odd = expand_from_center(i, i)
        even = expand_from_center(i, i + 1)

        if len(odd) > len(max_str):
            max_str = odd
        if len(even) > len(max_str):
            max_str = even

    return max_str''',
                          test_cases=json.dumps([
                              {
                                  "input": {"s": "babad"},
                                  "expected_output": "bab"
                              },
                              {
                                  "input": {"s": "cbbd"},
                                  "expected_output": "bb"
                              }
                          ]),
                          function_signature="def longestPalindrome(s: str) -> str:")
        self.db.session.merge(python_)
        python_ = Problem(Id=7,
                          title="Regular Expression Matching",
                          difficulty="Hard",
                          description="Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:'.' Matches any single character.​​​​'*' Matches zero or more of the preceding element.The matching should cover the entire input string (not partial).",
                          example_input='s = "aa", p = "a"',
                          example_output="false",
                          explanation='Explanation: "a" does not match the entire string "aa".',
                          type='python',solution_='''def isMatch(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i][j - 2] or (dp[i - 1][j] and (s[i - 1] == p[j - 2] or p[j - 2] == '.'))
            else:
                dp[i][j] = dp[i - 1][j - 1] and (s[i - 1] == p[j - 1] or p[j - 1] == '.')
    return dp[m][n]''',
                          test_cases=json.dumps([
                              {
                                  "input": {"s": "aa", "p": "a"},
                                  "expected_output": False
                              },
                              {
                                  "input": {"s": "aa", "p": "a*"},
                                  "expected_output": True
                              },
                              {
                                  "input": {"s": "ab", "p": ".*"},
                                  "expected_output": True
                              }
                          ]),
                          function_signature="def isMatch(s: str, p: str) -> bool:")
        python_ = Problem(Id=8,
                          title="Merge k Sorted Lists",
                          difficulty="Hard",
                          description="You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.Merge all the linked-lists into one sorted linked-list and return it.",
                          example_input='lists = [[1,4,5],[1,3,4],[2,6]]',
                          example_output="false",
                          explanation='The linked-lists are:[1->4->5,1->3->4,2->6]merging them into one sorted '
                                      'list:1->1->2->3->4->4->5->6',
                          type='python',solution_='''def list_to_linked_list(arr: List[int]) -> Optional[ListNode]:
    head = ListNode()
    current = head
    for val in arr:
        current.next = ListNode(val)
        current = current.next
    return head.next


def mergeKLists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    if not lists or len(lists) == 0:
        return None

    while len(lists) > 1:
        temp = []
        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            temp.append(merge_lists(l1, l2))
        lists = temp

    return lists[0]


def merge_lists(l1: ListNode, l2: ListNode) -> ListNode:
    node = ListNode()
    ans = node

    while l1 and l2:
        if l1.val > l2.val:
            node.next = l2
            l2 = l2.next
        else:
            node.next = l1
            l1 = l1.next
        node = node.next

    if l1:
        node.next = l1
    else:
        node.next = l2

    return ans.next


def get_final_results(lists: List[Optional[ListNode]])-> Optional[ListNode]:
    linked_lists = [list_to_linked_list(lst) for lst in lists]

    # Merging k sorted linked lists
    result = mergeKLists(linked_lists)

    # Converting result linked list back to a regular Python list for display
    output = []
    while result:
        output.append(result.val)
        result = result.next
    return output  # Inject user code
''',
                          test_cases=json.dumps([
                              {
                                  "input": {"lists": [[1, 4, 5], [1, 3, 4], [2, 6]]},
                                  "expected_output": [1, 1, 2, 3, 4, 4, 5, 6]
                              },
                              {
                                  "input": {"lists": []},
                                  "expected_output": []
                              },
                              {
                                  "input": {"lists": [[]]},
                                  "expected_output": []
                              }
                          ]),
                          function_signature="def get_final_results(input_lists: List[Optional[ListNode]])-> Optional["
                                             "ListNode]:")

        # python_ = Problem(Id=9,
        #                   title="Combine Two Tables",
        #                   difficulty="Hard",
        #                   description="Write a solution to report the first name, last name, city, and state of each "
        #                               "person in the Person table. If the address of a personId is not present in the "
        #                               "Address table, report null instead.Return the result table in any order.The "
        #                               "result format is in the following example.",
        #                   example_input='lists = [[1,4,5],[1,3,4],[2,6]]',
        #                   example_output="false",
        #                   explanation='The linked-lists are:[1->4->5,1->3->4,2->6]merging them into one sorted '
        #                               'list:1->1->2->3->4->4->5->6',
        #                   type='python',solution_='',
        #                   test_cases=json.dumps([
        #                       {
        #                           "input": {"lists": [[1, 4, 5], [1, 3, 4], [2, 6]]},
        #                           "expected_output": [1, 1, 2, 3, 4, 4, 5, 6]
        #                       },
        #                       {
        #                           "input": {"lists": []},
        #                           "expected_output": []
        #                       },
        #                       {
        #                           "input": {"lists": [[]]},
        #                           "expected_output": []
        #                       }
        #                   ]),
        #                   function_signature="def get_final_results(input_lists: List[Optional[ListNode]])-> Optional["
        #                                      "ListNode]:")
        # self.db.session.merge(python_)

    def add_sqlproblems(self):
        example_input = (
            "Person table:\n"
            "+----------+----------+-----------+\n"
            "| personId | lastName | firstName |\n"
            "+----------+----------+-----------+\n"
            "|    1     |  Wang    |   Allen   |\n"
            "|    2     |  Alice   |    Bob    |\n"
            "+----------+----------+-----------+"
            "                                          Address table:\n"
            "+-----------+----------+--------------+-------------+\n"
            "| addressId | personId |     city     |    state    |\n"
            "+-----------+----------+--------------+-------------+\n"
            "|     1     |    2     | New York City| New York    |\n"
            "|     2     |    3     |  Leetcode    | California  |\n"
            "+-----------+----------+--------------+-------------+"
        )
        example_output = (
            "+-----------+----------+--------------+-------------+\n"
            "| firstName | lastName |     city     |    state    |\n"
            "+-----------+----------+--------------+-------------+\n"
            "|   Allen   |   Wang   |     Null     |    Null     |\n"
            "|    Bob    |  Alice   | New York City|  New York   |\n"
            "+-----------+----------+--------------+-------------+"
        )

        python_ = Problem(Id=9,
                          title="Combine Two Tables",
                          difficulty="Hard",
                          description="Write a solution to report the first name, last name, city, and state of each "
                                      "person in the Person table. If the address of a personId is not present in the "
                                      "Address table, report null instead.Return the result table in any order.The "
                                      "result format is in the following example.",
                          example_input=example_input,
                          example_output=example_output,
                          explanation='There is no address in the address table for the personId = 1 so we return '
                                      'null in their city and state.addressId = 1 contains information about the '
                                      'address of personId = 2.',
                          type='sql',solution_='''SELECT P.firstName, P.lastName, A.city, A.state
FROM Person P LEFT JOIN Address A
on P.personId = A.personId''',
                          test_cases=json.dumps([
                              {
                                  "input": [
                                      "CREATE TABLE Person (personId INT, lastName VARCHAR(50), firstName VARCHAR(50));",
                                      "CREATE TABLE Address (addressId INT, personId INT, city VARCHAR(50), "
                                      "state VARCHAR(50));",
                                      "INSERT INTO Person (personId, lastName, firstName) VALUES (1, 'Wang', "
                                      "'Allen'), (2, 'Alice', 'Bob');",
                                      "INSERT INTO Address (addressId, personId, city, state) VALUES (1, 2, 'New York "
                                      "City', 'New York'), (2, 3, 'Leetcode', 'California'); "
                                  ],
                                  "expected_output": [
                                      {"firstName": "Allen", "lastName": "Wang", "city": None, "state": None},
                                      {"firstName": "Bob", "lastName": "Alice", "city": "New York City",
                                       "state": "New York"}
                                  ]
                              }
                          ]),
                          function_signature="# Write your MySQL query statement below ")
        self.db.session.merge(python_)
        example_input = (
            "Employee table:\n"
            "+----+--------+\n"
            "| id | salary |\n"
            "+----+--------+\n"
            "| 1  |  100   |\n"
            "| 2  |  200   |\n"
            "| 3  |  300   |\n"
            "+----+--------+"
        )

        example_output = (
            "+---------------------+\n"
            "| SecondHighestSalary |\n"
            "+---------------------+\n"
            "|        200          |\n"
            "+---------------------+"
        )
        python_ = Problem(Id=10,
                          title="Second Highest Salary",
                          difficulty="Medium",
                          description="Write a solution to find the second highest distinct salary from the Employee table. If there is no second highest salary, return null (return None in Pandas).The result format is in the following example.",
                          example_input=example_input,
                          example_output=example_output,
                          explanation='',
                          type='sql',solution_='''select
(select distinct Salary 
from Employee order by salary desc 
limit 1 offset 1) 
as SecondHighestSalary;''',
                          test_cases=json.dumps([
                              {
                                  "input": [
                                      "CREATE TABLE Employee (id INT, salary INT);",
                                      "INSERT INTO Employee (id, salary) VALUES (1, 100), (2, 200), (3, 300);"
                                  ],
                                  "expected_output": [{"SecondHighestSalary": 200}]
                              },
                              {
                                  "input": [
                                      "CREATE TABLE Employee (id INT, salary INT);",
                                      "INSERT INTO Employee (id, salary) VALUES (1, 100);"
                                  ],
                                  "expected_output": [{"SecondHighestSalary": None}]
                              }
                          ]),
                          function_signature="# Write your MySQL query statement below ")
        self.db.session.merge(python_)
        example_input = (
            "Employee table:\n"
            "+----+--------+--------+--------------+\n"
            "| id |  name  | salary | departmentId |\n"
            "+----+--------+--------+--------------+\n"
            "|  1 |  Joe   |  85000 |      1       |\n"
            "|  2 |  Henry |  80000 |      2       |\n"
            "|  3 |  Sam   |  60000 |      2       |\n"
            "|  4 |  Max   |  90000 |      1       |\n"
            "|  5 | Janet  |  69000 |      1       |\n"
            "|  6 | Randy  |  85000 |      1       |\n"
            "|  7 |  Will  |  70000 |      1       |\n"
            "+----+--------+--------+--------------+\n\n"
            "Department table:\n"
            "+----+--------+\n"
            "| id |  name  |\n"
            "+----+--------+\n"
            "|  1 |   IT   |\n"
            "|  2 |  Sales |\n"
            "+----+--------+"
        )

        example_output = (
            "+------------+---------+--------+\n"
            "| department | employee| salary |\n"
            "+------------+---------+--------+\n"
            "|     IT     |   Max   | 90000  |\n"
            "|     IT     |   Joe   | 85000  |\n"
            "|     IT     |  Randy  | 85000  |\n"
            "|    Sales   |  Henry  | 80000  |\n"
            "|    Sales   |   Sam   | 60000  |\n"
            "+------------+---------+--------+"
        )
        python_ = Problem(Id=11,
                          title="Department Top Three Salaries",
                          difficulty="Hard",
                          description="A company's executives are interested in seeing who earns the most money in each of the company's departments. A high earner in a department is an employee who has a salary in the top three unique salaries for that department.Write a solution to find the employees who are high earners in each of the departments.Return the result table in any order.The result format is in the following example.",
                          example_input=example_input,
                          example_output=example_output,
                          explanation='In the IT department:\n- Max earns the highest unique salary\n- Both Randy and Joe earn the second-highest unique salary\n- Will earns the third-highest unique salary\nIn the Sales department:\n- Henry earns the highest salary\n- Sam earns the second-highest salary\n- There is no third-highest salary as there are only two employees',
                          type='sql',solution_='''SELECT
    d.name AS department,
    e.name AS employee,
    e.salary AS salary
FROM
    Employee e
    JOIN Department d ON e.departmentId = d.id
WHERE
    (
        SELECT COUNT(DISTINCT salary)
        FROM Employee e2
        WHERE e2.departmentId = e.departmentId AND e2.salary >= e.salary
    ) <= 3
ORDER BY
    department, salary DESC;''',
                          test_cases=json.dumps([
                              {
                                  "input": [
                                      "CREATE TABLE Employee (id INT, name VARCHAR(50), salary INT, departmentId INT);",
                                      "CREATE TABLE Department (id INT, name VARCHAR(50));",
                                      "INSERT INTO Employee (id, name, salary, departmentId) VALUES "
                                      "(1, 'Joe', 85000, 1), (2, 'Henry', 80000, 2), (3, 'Sam', 60000, 2), "
                                      "(4, 'Max', 90000, 1), (5, 'Janet', 69000, 1), (6, 'Randy', 85000, 1), (7, "
                                      "'Will', 70000, 1);",
                                      "INSERT INTO Department (id, name) VALUES (1, 'IT'), (2, 'Sales');"
                                  ],
                                  "expected_output": [
                                      {"department": "IT", "employee": "Max", "salary": 90000},
                                      {"department": "IT", "employee": "Joe", "salary": 85000},
                                      {"department": "IT", "employee": "Randy", "salary": 85000},
                                      {"department": "IT", "employee": "Will", "salary": 70000},
                                      {"department": "Sales", "employee": "Henry", "salary": 80000},
                                      {"department": "Sales", "employee": "Sam", "salary": 60000}
                                  ]
                              }
                          ]),
                          function_signature="# Write your MySQL query statement below ")
        self.db.session.merge(python_)
        example_input = (
            "Stadium table:\n"
            "+----+------------+--------+\n"
            "| id | visit_date | people |\n"
            "+----+------------+--------+\n"
            "|  1 | 2017-01-01 |   10   |\n"
            "|  2 | 2017-01-02 |  109   |\n"
            "|  3 | 2017-01-03 |  150   |\n"
            "|  4 | 2017-01-04 |   99   |\n"
            "|  5 | 2017-01-05 |  145   |\n"
            "|  6 | 2017-01-06 | 1455   |\n"
            "|  7 | 2017-01-07 |  199   |\n"
            "|  8 | 2017-01-08 |  188   |\n"
            "+----+------------+--------+"
        )

        example_output = (
            "+----+------------+--------+\n"
            "| id | visit_date | people |\n"
            "+----+------------+--------+\n"
            "|  5 | 2017-01-05 |  145   |\n"
            "|  6 | 2017-01-06 | 1455   |\n"
            "|  7 | 2017-01-07 |  199   |\n"
            "|  8 | 2017-01-08 |  188   |\n"
            "+----+------------+--------+"
        )

        python_ = Problem(Id=12,
                          title="Human Traffic of Stadium",
                          difficulty="Hard",
                          description="Write a solution to display the records with three or more rows with consecutive id's, and the number of people is greater than or equal to 100 for each.Return the result table ordered by visit_date in ascending order.The result format is in the following example.",
                          example_input=example_input,
                          example_output=example_output,
                          explanation='The four rows with ids 5, 6, 7, and 8 have consecutive ids and each of them has >= 100 people attended. Note that row 8 was included even though the visit_date was not the next day after row 7.The rows with ids 2 and 3 are not included because we need at least three consecutive ids.',
                          type='sql',solution_='''# Write your MySQL query statement below
with q1 as (
select *, 
     count(*) over( order by id range between current row and 2 following ) following_cnt,
     count(*) over( order by id range between 2 preceding and current row ) preceding_cnt,
     count(*) over( order by id range between 1 preceding and 1 following ) current_cnt
from stadium
where people > 99
)
select id, visit_date, people
from q1
where following_cnt = 3 or preceding_cnt = 3 or current_cnt = 3
order by visit_date''',
                          test_cases=json.dumps([
                              {
                                  "input": [
                                      "CREATE TABLE stadium (id INT, visit_date DATE, people INT);",
                                      "INSERT INTO stadium (id, visit_date, people) VALUES "
                                      "(1, '2017-01-01', 10), (2, '2017-01-02', 109), (3, '2017-01-03', 150), "
                                      "(4, '2017-01-04', 99), (5, '2017-01-05', 145), (6, '2017-01-06', 1455), "
                                      "(7, '2017-01-07', 199), (8, '2017-01-08', 188);"
                                  ],
                                  "expected_output": [
                                      {"id": 5, "visit_date": "2017-01-05", "people": 145},
                                      {"id": 6, "visit_date": "2017-01-06", "people": 1455},
                                      {"id": 7, "visit_date": "2017-01-07", "people": 199},
                                      {"id": 8, "visit_date": "2017-01-08", "people": 188}
                                  ]
                              }
                          ]),
                          function_signature="# Write your MySQL query statement below ")

        self.db.session.merge(python_)
