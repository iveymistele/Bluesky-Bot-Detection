# DS 4320 Project 1: Detecting Likely Automated Bluesky Accounts 


**Executive Summary fix**
This project uses short-term activity and content signals from real-time data streams from the Bluesky social media platform. 

**Ivey Mistele**

**zyh4up**

**DOI to do**

**Press Release:** [Link]

**Data:** [Link](https://myuva-my.sharepoint.com/:f:/g/personal/zyh4up_virginia_edu/IgDohLMCAK-RRKmYPl1QViVRAel_N3mQHVozNomswaI5pbc?e=pCEpvf)

**Pipeline:** [Link]

License Name: Link

## Problem Definition

**General Problem:**  Identifying automated social media accounts (bots).

**Refined Problem Statement:** Developing a model to identify accounts on Bluesky that are likely automated (bots) using engagement patterns, posting behavior, and text features. 

**Rationale:** 

    I chose to focus on Bluesky because it provides publicly accessible, real-time data through the firehose API, which made it feasible to collect a large and relevant dataset for analysis. Compared to other platforms with more restrictive APIs, this allowed me to work directly with live social media activity rather than relying on pre-collected datasets. I refined the problem to focus on bot detection because automated accounts often follow similarly distinct behavioral patterns. I used features that are available in the data, like posting frequency, reply behavior, and text features like hashtags and links. These features represent account interaction with the platform, which potentially differs between bots and human accounts. By focusing on existing patterns in behavior and content, the model aims to identify accounts that act in ways that are more consistent with automated activity, even without explicitly labeled training data.

**Project Motivation:** 
 

 Bots make up lots **statistic?** of internet traffic. Identifying these bots is important in not only identifying promotional or spam material on social media, but also can serve as a useful tool for businesses to use to attempt to combat the amount of automated accounts on their platofmr. can be harmful because yeahj 

 **Press Release: Kill the Bots in your Platform idk or for personal use report em**

[Link to Press Release]()

## Domain Exposition 

**Terminology**

| Term | Explanation |
|---|---|
|Account (DID)| A unique Bluesky user identifier used to group posts by user. |
|Post| A single message created by a user in the Bluesky platform. |
|Bot-like Account | An account exhibiting automated/non-human behavioral patterns. |
|Human-like Account | An account exhibiting natural human behavior (conversational). |
|Reply Rate | Proportion of Bluesky posts that are replies; proxy for conversational engagement. |
|URL Rate | Proportion of posts containing links; often higher in promotional or automated accounts. |
|Hashtag Rate | Frequency of hashtag usage in posts. |
|Mention Rate | Frequency of tagging other users in posts. |
|Average Post Length| Average character length of posts for an account. |
|Total Posts| Number of posts observed for an account during the collection window. |
|Label | Binary classification (1 = likely bot, 0 = likely human, None = inconclusive). |
|Cluster | Group assignment from unsupervised KMeans clustering. | 

**Key Metrics (KPIs)**

| Metric | Purpose |
|---|---|
|Accuracy| Overall correctness of the classifier on unseen data. |
|Precision| How many predicted bots are actually bot-like. |
|Recall| How many bot-like accounts are successfully identified. | 
|F1 Score| Balance between precision and recall. | 
|Feature Coefficients| Indicate which behaviors are most associated with bot-like accounts. |

**Project Domain**

This project falls within the broader domain of bot detection on social media. The goal in this space is to identify accounts that are likely automated rather than human, usually based on patterns in behavior, activity, and interaction. This is important because bots can influence conversations, spread spam or misinformation, and distort engagement metrics. My project looks at this problem specifically in the context of Bluesky, using behavioral data to approximate which accounts might be bot-like.

**Background Readings:** [Link](https://myuva-my.sharepoint.com/:f:/g/personal/zyh4up_virginia_edu/IgDtRN1JEgtmSqAeFWx2VAQ-AYCNCmTYpc_DqgbPrcGhEyI?e=NX7sbn)

**Reading Summary**

| Title of Article | Description | Link |
|---|---|---|
|Social Media Bots Infographic Set|A set of informative infographics defining "bot" account behavior and warning signs made by the US Cybersecurity and Infrastructure Security Agency. | https://myuva-my.sharepoint.com/:b:/g/personal/zyh4up_virginia_edu/IQDkTME9CtjuQ6kqDxbh46-RAXILmNvZvw-YGKZLFG8Qehg?e=TC4Rfc |
| What is a social media bot? Social media bot definition | An article by Cloudfare defining social media bots and their objectives. | https://myuva-my.sharepoint.com/:u:/r/personal/zyh4up_virginia_edu/Documents/DBD%20Project%201/Background%20Reading/Social%20Media%20Bot%20Definition.url?csf=1&web=1&e=W3kdtc |
| Social media platforms aren't doing enough to stop harmful AI bots, research finds | An article describing research from the University of Notre Dame on the AI bot policies of several major social media platforms. | https://myuva-my.sharepoint.com/:u:/r/personal/zyh4up_virginia_edu/Documents/DBD%20Project%201/Background%20Reading/Social%20Media%20Bot%20Definition.url?csf=1&web=1&e=W3kdtc |
| A global comparison of social media bot and human characteristics | A scientific article published analyzing three challenges of studying bot detection: systematic detection, differentiation of harmful/beneficial behavior, and restriction of harmful bots. | https://myuva-my.sharepoint.com/:u:/r/personal/zyh4up_virginia_edu/Documents/DBD%20Project%201/Background%20Reading/A%20global%20comparison%20of%20social%20media%20bot%20and%20human%20characteristics.url?csf=1&web=1&e=rOREwc |
| Understanding the Influence of Social Media Bots | An article from ICUC explaining the importance of bot detection in social media. | https://myuva-my.sharepoint.com/:u:/r/personal/zyh4up_virginia_edu/Documents/DBD%20Project%201/Background%20Reading/Understanding%20the%20influence%20of%20social%20media%20bot%20accounts.url?csf=1&web=1&e=z4uQyj |

## Data Creation

**Provenance**

I collected the raw data using the publically available Bluesky Firehose API. I wrote my own ingestion [script](Link To repo)