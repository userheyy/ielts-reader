"""Replace assisted/reconstructed C17 question prompts with PDF-original wording."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSAGES = ROOT / "data" / "passages"


def br(lines: list[str]) -> str:
    return "<br>".join(lines)


ORIGINALS = {
    "c17-test2-p1": {
        "title": "Questions 1–13 · Notes completion + TRUE/FALSE/NOT GIVEN",
        "instructions": [
            "Questions 1–5: Complete the notes below. Choose ONE WORD ONLY from the passage for each answer.",
            "Questions 6–13: Do the following statements agree with the information given in Reading Passage 1?",
        ],
        "prompts": {
            1: "heard a noise of breaking when one teenager threw a ___",
            2: "teenagers went into the ___ and found a number of containers",
            3: "containers made of ___",
            4: "thought to have been written by group of people known as the ___",
            5: "written mainly in the ___ language",
            6: "The Bedouin teenagers who found the scrolls were disappointed by how little money they received for them.",
            7: "There is agreement among academics about the origin of the Dead Sea Scrolls.",
            8: "Most of the books of the Bible written on the scrolls are incomplete.",
            9: "The information on the Copper Scroll is written in an unusual way.",
            10: "Mar Samuel was given some of the scrolls as a gift.",
            11: "In the early 1950s, a number of educational establishments in the US were keen to buy scrolls from Mar Samuel.",
            12: "The scroll that was pieced together in 2017 contains information about annual occasions in the Qumran area 2,000 years ago.",
            13: "Academics at the University of Haifa are currently researching how to decipher the final scroll.",
        },
    },
    "c17-test2-p2": {
        "title": "Questions 14–26 · Matching information/researchers + sentence completion",
        "instructions": [
            "Questions 14–18: Reading Passage 2 has five sections, A–E. Which section contains the following information?",
            "Questions 19–23: Match each statement with the correct researcher, A–D. A Jorg Kudla; B Caixia Gao; C Joyce Van Eck; D Jonathan Jones.",
            "Questions 24–26: Complete the sentences below. Choose ONE WORD ONLY from the passage for each answer.",
        ],
        "prompts": {
            14: "a reference to a type of tomato that can resist a dangerous infection",
            15: "an explanation of how problems can arise from focusing only on a certain type of tomato plant",
            16: "a number of examples of plants that are not cultivated at present but could be useful as food sources",
            17: "a comparison between the early domestication of the tomato and more recent research",
            18: "a personal reaction to the flavour of a tomato that has been genetically edited",
            19: "Domestication of certain plants could allow them to adapt to future environmental challenges.",
            20: "The idea of growing and eating unusual plants may not be accepted on a large scale.",
            21: "It is not advisable for the future direction of certain research to be made public.",
            22: "Present efforts to domesticate one wild fruit are limited by the costs involved.",
            23: "Humans only make use of a small proportion of the plant food available on Earth.",
            24: "An undesirable trait such as loss of ___ may be caused by a mutation in a tomato gene.",
            25: "By modifying one gene in a tomato plant, researchers made the tomato three times its original ___.",
            26: "A type of tomato which was not badly affected by ___, and was rich in vitamin C, was produced by a team of researchers in China.",
        },
    },
    "c17-test2-p3": {
        "title": "Questions 27–40 · Multiple choice + YES/NO/NOT GIVEN + summary",
        "instructions": [
            "Questions 27–31: Choose the correct letter, A, B, C or D.",
            "Questions 32–36: Do the following statements agree with the claims of the writer in Reading Passage 3?",
            "Questions 37–40: Complete the summary using the list of words, A–G.",
        ],
        "prompts": {
            27: br(["The purpose of the first paragraph is to", "A defend particular ideas.", "B compare certain beliefs.", "C disprove a widely held view.", "D outline a common assumption."]),
            28: br(["What are the writers doing in the second paragraph?", "A criticising an opinion", "B justifying a standpoint", "C explaining an approach", "D supporting an argument"]),
            29: br(["In the third paragraph, what do the writers suggest about Darwin and Einstein?", "A They represent an exception to a general rule.", "B Their way of working has been misunderstood.", "C They are an ideal which others should aspire to.", "D Their achievements deserve greater recognition."]),
            30: br(["John Nicholson is an example of a person whose idea", "A established his reputation as an influential scientist.", "B was only fully understood at a later point in history.", "C laid the foundations for someone else’s breakthrough.", "D initially met with scepticism from the scientific community."]),
            31: br(["What is the key point of interest about the ‘acey-deucy’ stirrup placement?", "A the simple reason why it was invented", "B the enthusiasm with which it was adopted", "C the research that went into its development", "D the cleverness of the person who first used it"]),
            32: "Acknowledging people such as Plato or da Vinci as geniuses will help us understand the process by which great minds create new ideas.",
            33: "The Law of Effect was discovered at a time when psychologists were seeking a scientific reason why creativity occurs.",
            34: "The Law of Effect states that no planning is involved in the behaviour of organisms.",
            35: "The Law of Effect sets out clear explanations about the sources of new ideas and behaviours.",
            36: "Many scientists are now turning away from the notion of intelligent design and genius.",
            37: br(["The traditional view of scientific discovery is that breakthroughs happen when a single great mind has sudden ___.", "A invention B goals C compromise D mistakes E luck F inspiration G experiments"]),
            38: "In some cases, this process involves ___, such as Nicholson’s theory about proto-elements.",
            39: "There is also often an element of ___, for example, the coincidence of ideas that led to the invention of the Post-It note.",
            40: "With both the Law of Natural Selection and the Law of Effect, there may be no clear ___ involved, but merely a process of variation and selection.",
        },
    },
    "c17-test3-p1": {
        "title": "Questions 1–13 · Notes completion + TRUE/FALSE/NOT GIVEN",
        "instructions": [
            "Questions 1–5: Complete the notes below. Choose ONE WORD ONLY from the passage for each answer.",
            "Questions 6–13: Do the following statements agree with the information given in Reading Passage 1?",
        ],
        "prompts": {
            1: "ate an entirely ___ diet",
            2: "probably depended mainly on ___ when hunting",
            3: "young spent first months of life inside its mother’s ___",
            4: "last evidence in mainland Australia is a 3,100-year-old ___",
            5: "reduction in ___ and available sources of food were partly responsible for decline in Tasmania",
            6: "Significant numbers of thylacines were killed by humans from the 1830s onwards.",
            7: "Several thylacines were born in zoos during the late 1800s.",
            8: "John Gould’s prediction about the thylacine surprised some biologists.",
            9: "In the early 1900s, many scientists became worried about the possible extinction of the thylacine.",
            10: "T. T. Flynn’s proposal to rehome captive thylacines on an island proved to be impractical.",
            11: "There were still reasonable numbers of thylacines in existence when a piece of legislation protecting the species during their breeding season was passed.",
            12: "From 1930 to 1936, the only known living thylacines were all in captivity.",
            13: "Attempts to find living thylacines are now rarely made.",
        },
    },
    "c17-test3-p2": {
        "title": "Questions 14–26 · Matching information + multiple answers + sentence completion",
        "instructions": [
            "Questions 14–20: Reading Passage 2 has eight sections, A–H. Which section contains the following information?",
            "Questions 21 and 22: Choose TWO letters, A–E.",
            "Questions 23–26: Complete the sentences below. Choose NO MORE THAN TWO WORDS from the passage for each answer.",
        ],
        "prompts": {
            14: "examples of a range of potential environmental advantages of oil palm tree cultivation",
            15: "description of an organisation which controls the environmental impact of palm oil production",
            16: "examples of the widespread global use of palm oil",
            17: "reference to a particular species which could benefit the ecosystem of oil palm plantations",
            18: "figures illustrating the rapid expansion of the palm oil industry",
            19: "an economic justification for not opposing the palm oil industry",
            20: "examples of creatures badly affected by the establishment of oil palm plantations",
            21: br(["Which TWO statements are made about the Roundtable on Sustainable Palm Oil (RSPO)?", "A Its membership has grown steadily over the course of the last decade.", "B It demands that certified producers be open and honest about their practices.", "C It took several years to establish its set of criteria for sustainable palm oil certification.", "D Its regulations regarding sustainability are stricter than those governing other industries.", "E It was formed at the request of environmentalists concerned about the loss of virgin forests."]),
            22: "Same question as 21: choose the second correct statement about the Roundtable on Sustainable Palm Oil (RSPO).",
            23: "One advantage of palm oil for manufacturers is that it stays ___ even when not refrigerated.",
            24: "The ___ is the best known of the animals suffering habitat loss as a result of the spread of oil palm plantations.",
            25: "As one of its criteria for the certification of sustainable palm oil, the RSPO insists that growers check ___ on a routine basis.",
            26: "Ellwood and his researchers are looking into whether the bird’s nest fern could restore ___ in areas where oil palm trees are grown.",
        },
    },
    "c17-test3-p3": {
        "title": "Questions 27–40 · Multiple choice + YES/NO/NOT GIVEN + summary",
        "instructions": [
            "Questions 27–31: Choose the correct letter, A, B, C or D.",
            "Questions 32–35: Do the following statements agree with the claims of the writer in Reading Passage 3?",
            "Questions 36–40: Complete the summary using the list of phrases, A–J.",
        ],
        "prompts": {
            27: br(["What point does Shester make about Barr’s book in the first paragraph?", "A It gives a highly original explanation for urban development.", "B Elements of Barr’s research papers are incorporated throughout the book.", "C Other books that are available on the subject have taken a different approach.", "D It covers a range of factors that affected the development of New York."]),
            28: br(["How does Shester respond to the information in the book about tenements?", "A She describes the reasons for Barr’s interest.", "B She indicates a potential problem with Barr’s analysis.", "C She compares Barr’s conclusion with that of other writers.", "D She provides details about the sources Barr used for his research."]),
            29: br(["What does Shester say about chapter six of the book?", "A It contains conflicting data.", "B It focuses too much on possible trends.", "C It is too specialised for most readers.", "D It draws on research that is out of date."]),
            30: br(["What does Shester suggest about the chapters focusing on the 1920s building boom?", "A The information should have been organised differently.", "B More facts are needed about the way construction was financed.", "C The explanation that is given for the building boom is unlikely.", "D Some parts will have limited appeal to certain people."]),
            31: br(["What impresses Shester the most about the chapter on land values?", "A the broad time period that is covered", "B the interesting questions that Barr asks", "C the nature of the research into the topic", "D the recommendations Barr makes for the future"]),
            32: "The description in the first chapter of how New York probably looked from the air in the early 1600s lacks interest.",
            33: "Chapters two and three prepare the reader well for material yet to come.",
            34: "The biggest problem for many nineteenth-century New York immigrant neighbourhoods was a lack of amenities.",
            35: "In the nineteenth century, New York’s immigrant neighbourhoods tended to concentrate around the harbour.",
            36: br(["In chapter seven, Barr indicates how the lack of bedrock close to the surface does not explain why skyscrapers are absent from ___.", "A development plans B deep excavations C great distance D excessive expense E impossible tasks F associated risks G water level H specific areas I total expenditure J construction guidelines"]),
            37: "He points out that although the cost of foundations increases when bedrock is deep below the surface, this cannot be regarded as ___.",
            38: "The cost of deep foundations cannot be regarded as excessive, especially when compared to ___.",
            39: "He describes not only how ___ are made possible by the use of caissons, but he also discusses their risks.",
            40: "He discusses their ___.",
        },
    },
    "c17-test4-p1": {
        "title": "Questions 1–13 · TRUE/FALSE/NOT GIVEN + table completion",
        "instructions": [
            "Questions 1–6: Do the following statements agree with the information given in Reading Passage 1?",
            "Questions 7–13: Complete the table below. Choose ONE WORD ONLY from the passage for each answer.",
        ],
        "prompts": {
            1: "Many Madagascan forests are being destroyed by attacks from insects.",
            2: "Loss of habitat has badly affected insectivorous bats in Madagascar.",
            3: "Ricardo Rocha has carried out studies of bats in different parts of the world.",
            4: "Habitat modification has resulted in indigenous bats in Madagascar becoming useful to farmers.",
            5: "The Malagasy mouse-eared bat is more common than other indigenous bat species in Madagascar.",
            6: "Bats may feed on paddy swarming caterpillars and grass webworms.",
            7: "Method: DNA analysis of bat ___",
            8: "Findings: the bats ate pests of rice, ___, sugarcane, nuts and fruit",
            9: "Findings: the bats prevent the spread of disease by eating ___ and blackflies",
            10: "Local attitudes: bats provide food rich in ___",
            11: "Local attitudes: the buildings where they roost become ___",
            12: "Local attitudes: they play an important role in local ___",
            13: "Recommendation: farmers should provide special ___ to support the bat population",
        },
    },
    "c17-test4-p2": {
        "title": "Questions 14–26 · Matching information + summary + multiple answers",
        "instructions": [
            "Questions 14–18: Reading Passage 2 has six sections, A–F. Which section contains the following information?",
            "Questions 19–22: Complete the summary below. Choose ONE WORD from the passage for each answer.",
            "Questions 23–26: Choose TWO letters, A–E.",
        ],
        "prompts": {
            14: "an explanation of the need for research to focus on individuals with a fairly consistent income",
            15: "examples of the sources the database has been compiled from",
            16: "an account of one individual’s refusal to obey an order",
            17: "a reference to a region being particularly suited to research into the link between education and economic growth",
            18: "examples of the items included in a list of personal possessions",
            19: "The database that Ogilvie and her team has compiled sheds light on the lives of a range of individuals, as well as those of their ___, over a 300-year period.",
            20: "Ana Regina and Magdalena Riethmüllerin were reprimanded for reading while they should have been paying attention to a ___.",
            21: "Juliana Schweickherdt was later given a ___ as a punishment.",
            22: "Cases like this illustrate how the guilds could prevent ___ and stop skilled people from working.",
            23: br(["Which TWO of the following statements does the writer make about literacy rates in Section B?", "A Very little research has been done into the link between high literacy rates and improved earnings.", "B Literacy rates in Germany between 1600 and 1900 were very good.", "C There is strong evidence that high literacy rates in the modern world result in economic growth.", "D England is a good example of how high literacy rates helped a country industrialise.", "E Economic growth can help to improve literacy rates."]),
            24: "Same question as 23: choose the second correct statement about literacy rates in Section B.",
            25: br(["Which TWO of the following statements does the writer make in Section F about guilds in German-speaking Central Europe between 1600 and 1900?", "A They helped young people to learn a skill.", "B They were opposed to people moving to an area for work.", "C They kept better records than guilds in other parts of the world.", "D They opposed practices that threatened their control over a trade.", "E They predominantly consisted of wealthy merchants."]),
            26: "Same question as 25: choose the second correct statement about guilds in German-speaking Central Europe between 1600 and 1900.",
        },
    },
    "c17-test4-p3": {
        "title": "Questions 27–40 · Matching information + TRUE/FALSE/NOT GIVEN + summary",
        "instructions": [
            "Questions 27–32: Reading Passage 3 has eight paragraphs, A–H. Which paragraph contains the following information?",
            "Questions 33–36: Do the following statements agree with the information given in Reading Passage 3?",
            "Questions 37–40: Complete the summary below. Choose ONE WORD ONLY from the passage for each answer.",
        ],
        "prompts": {
            27: "a reference to earlier examples of blindfold chess",
            28: "an outline of what blindfold chess involves",
            29: "a claim that Gareyev’s skill is limited to chess",
            30: "why Gareyev’s skill is of interest to scientists",
            31: "an outline of Gareyev’s priorities",
            32: "a reason why the last part of a game may be difficult",
            33: "In the forthcoming games, all the participants will be blindfolded.",
            34: "Gareyev has won competitions in BASE jumping.",
            35: "UCLA is the first university to carry out research into blindfold chess players.",
            36: "Good chess players are likely to be able to play blindfold chess.",
            37: "The researchers started by testing Gareyev’s ___.",
            38: "He was required to recall a string of ___ in order and also in reverse order.",
            39: "Scans showed an unusual amount of ___ within the areas of Gareyev’s brain that are concerned with directing attention.",
            40: "The scans raised the possibility of unusual strength in the parts of his brain that deal with ___ input.",
        },
    },
}

# IELTS two-answer questions use one shared prompt for two answer boxes.
# Store the full PDF wording in both boxes so the web page never shows a
# reconstructed "same question" helper sentence.
ORIGINALS["c17-test3-p2"]["prompts"][22] = ORIGINALS["c17-test3-p2"]["prompts"][21]
ORIGINALS["c17-test4-p2"]["prompts"][24] = ORIGINALS["c17-test4-p2"]["prompts"][23]
ORIGINALS["c17-test4-p2"]["prompts"][26] = ORIGINALS["c17-test4-p2"]["prompts"][25]


def main() -> None:
    for pid, spec in ORIGINALS.items():
        path = PASSAGES / f"{pid}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        group = data["questions"][0]
        all_items = [item for existing_group in data["questions"] for item in existing_group["items"]]
        group["title"] = spec["title"]
        group["instructions"] = spec["instructions"]
        for item in all_items:
            item["prompt"] = spec["prompts"][item["number"]]

        if pid == "c17-test4-p3":
            evidence_fixes = {27: 5, 28: 3, 32: 31}
            for item in all_items:
                if item["number"] in evidence_fixes:
                    item["evidence_sentence"] = evidence_fixes[item["number"]]

        # Test 4 Passage 3 contains three genuinely separate IELTS tasks.
        # Keep their original boundaries and full directions instead of
        # presenting them as one synthetic "mixed" exercise.
        if pid == "c17-test4-p3":
            by_number = {item["number"]: item for item in all_items}
            data["questions"] = [
                {
                    "title": "Questions 27–32 · Matching information",
                    "type": "matching-information",
                    "instructions": [
                        "Reading Passage 3 has eight paragraphs, A–H.",
                        "Which paragraph contains the following information?",
                        "Write the correct letter, A–H, in boxes 27–32 on your answer sheet.",
                        "NB You may use any letter more than once.",
                    ],
                    "items": [by_number[n] for n in range(27, 33)],
                },
                {
                    "title": "Questions 33–36 · TRUE / FALSE / NOT GIVEN",
                    "type": "true-false-not-given",
                    "instructions": [
                        "Do the following statements agree with the information given in Reading Passage 3?",
                        "In boxes 33–36 on your answer sheet, write:",
                        "TRUE — if the statement agrees with the information",
                        "FALSE — if the statement contradicts the information",
                        "NOT GIVEN — if there is no information about this",
                    ],
                    "items": [by_number[n] for n in range(33, 37)],
                },
                {
                    "title": "Questions 37–40 · How the research was carried out",
                    "type": "summary-completion",
                    "instructions": [
                        "Complete the summary below.",
                        "Choose ONE WORD ONLY from the passage for each answer.",
                        "Write your answers in boxes 37–40 on your answer sheet.",
                    ],
                    "items": [by_number[n] for n in range(37, 41)],
                },
            ]
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(pid, "updated")


if __name__ == "__main__":
    main()
