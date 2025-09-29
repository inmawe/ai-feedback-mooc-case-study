# AI-Mediated Feedback in MOOC Case Study

This repository serves as the **main entry point** for our study on AI-mediated feedback in a MOOC case study (submitted to LAK 2026).  
The project investigates whether personalized, AI-generated feedback improves learners’ self-efficacy, motivation, feedback perception, and performance in SQL and machine learning tasks.  

## 📚 Context
The intervention was implemented in the MITx *Supply Chain Technology and Systems* MOOC.  
Learners worked on a case study involving SQL queries and machine learning tasks.  
- **Control group**: received static, pre-authored explanations.  
- **Treatment group**: received real-time, AI-generated personalized feedback.  

## ⚙️ Implementation Notes
The AI-mediated feedback was implemented using **Streamlit apps**, each corresponding to a case study question.  
- Learners in the Treatment group interacted with these apps, which provided **real-time, AI-generated feedback**.  
- Apps were then **embedded into the edX platform** via iframes, so learners could complete the exercises seamlessly inside the MOOC environment.  

## 🔗 Repositories

- [SQL Question 1: Basic Data Retrieval](https://github.com/MITx-CTL-SC4x/w10-caseStudy-sql1)  
- [SQL Question 2: Intermediate Querying](https://github.com/MITx-CTL-SC4x/w10-caseStudy-sql2)  
- [SQL Question 3: Advanced SQL Joins](https://github.com/MITx-CTL-SC4x/w10-caseStudy-sql3)  
- [ML Question 1: Feature Selection](https://github.com/MITx-CTL-SC4x/w10-caseStudy-ml1)  
- [ML Question 2: Model Choice](https://github.com/MITx-CTL-SC4x/w10-caseStudy-ml2)  
- [ML Question 3: Interpretation](https://github.com/MITx-CTL-SC4x/w10-caseStudy-ml3)  

## 📝 Citation
If you use this material, please cite our LAK 2026 paper:  

```bibtex
@inproceedings{author12026ai,
  author    = {Author1 and Author2},
  title     = {Does AI Feedback Improve Learning in MOOCs? Findings from a Randomized Trial},
  booktitle = {Proceedings of the 16th International Conference on Learning Analytics \& Knowledge (LAK 2026)},
  year      = {2026},
  publisher = {ACM},
  doi       = {10.1145/XXXXXXX.XXXXXXX}
}
