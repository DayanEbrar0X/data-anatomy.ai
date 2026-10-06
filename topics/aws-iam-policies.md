# How AWS decides allow or deny

<img src="https://img.shields.io/badge/Cloud-0369A1?style=flat-square" alt="Cloud"> <img src="https://img.shields.io/badge/status-planned-B45309?style=flat-square" alt="planned">

> Your Lambda has permission, and AWS still says Access Denied.

## The idea

Every AWS request is checked against the policies that apply to it. Everything starts as an implicit deny, an allow can grant access, and an explicit deny anywhere overrides every allow.

Knowing that order, plus where policies come from (identity, resource, permission boundaries, organization rules), turns Access Denied from a guessing game into a checklist.

## What the lesson will build

- A policy evaluator for a simplified set of rules
- Requests walked through allow, deny and default deny
- The same request failing because of a deny in another policy

## Key ideas

- Implicit and explicit deny
- Identity and resource policies
- Least privilege
- Reading an Access Denied error

## The video

- **Long form:** A request passing through a series of gates, each policy lighting green or red, until one red gate stops it.
- **Short:** One deny beats every allow.

When it's published, the code will live in [`cloud/`](../cloud) and this page will link to it.

---
[All topics](README.md) · [Suggest a topic](https://github.com/DayanEbrar0X/data-anatomy.ai/issues/new?title=Topic+idea%3A+)
