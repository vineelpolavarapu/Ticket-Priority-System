# Ticket-Priority-System

## Ticket Priority System

A backend system that automatically assigns priority levels to customer support tickets based on business rules such as issue severity, customer type, impact, and time.

## Problem Statement

In real customer support systems, tickets are not handled on a first-come basis.
Critical issues affecting enterprise customers must be prioritized over minor issues.

### Manual prioritization is:

error-prone

inconsistent

not scalable

This project solves that by automating ticket prioritization.

## Solution Overview

### The system:

Accepts ticket details via REST API

Calculates a priority score using defined rules

Assigns priority levels (P0–P3)

Persists ticket data in MySQL

Returns priority instantly to the requester

## Architecture
Client (Postman / Frontend) (*I use Postman*) → Flask API → Priority Engine : Business Rules →  MySQL Repository → Persistent Storage

## Tech Stack

**Language:** Python

**Framework**: Flask

**Database**: MySQL

**API Testing**: Postman

**Version Control**: Git & GitHub

## Priority Rules (*Example*)

Factor	Description
**Issue Type**	critical / major / minor
**Customer Type**	free / paid / enterprise
**Impact**	number of users affected
**Time**	ticket age

Final priority is calculated using weighted scoring.

## API Endpoints

Create Ticket
POST /tickets


Request Body

{
  "issue_type": "critical",
  "impact": 120,
  "customer_type": "enterprise"
}


Response

{
  "score": 15,
  "level": "P1"
}

## Database Schema

tickets table stores:

issue_type

impact

customer_type

created_at

priority_score

priority_level

## How to Run Locally

Clone the repo

Install dependencies

Configure MySQL

Run:

python app.py


Server runs on:

http://127.0.0.1:5000

## Future Enhancements

GET APIs for tickets

Pagination & filtering

Authentication

Deployment

## Author

Vineel Kumar Polavarapu
Aspiring Software Engineer