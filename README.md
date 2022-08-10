# Snippet Analizer

[![Build](https://github.com/WebGoat/WebGoat/actions/workflows/build.yml/badge.svg?branch=develop)](https://github.com/WebGoat/WebGoat/actions/workflows/build.yml)
[![java-jdk](https://img.shields.io/badge/java%20jdk-17-green.svg)](https://jdk.java.net/)
[![OWASP Labs](https://img.shields.io/badge/OWASP-Lab%20project-f7b73c.svg)](https://owasp.org/projects/)
[![GitHub release](https://img.shields.io/github/release/WebGoat/WebGoat.svg)](https://github.com/WebGoat/WebGoat/releases/latest)
[![Gitter](https://badges.gitter.im/OWASPWebGoat/community.svg)](https://gitter.im/OWASPWebGoat/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Discussions](https://img.shields.io/github/discussions/WebGoat/WebGoat)](https://github.com/WebGoat/WebGoat/discussions)

# Scopo

L'obbiettivo di questo progetto è stato quello di creare, attraverso, [DJANGO REST FRAMEWORK](https://www.django-rest-framework.org/) delle Web browsable API che permetessero di effettuare varie attività su snippet di codice scritti in Python. Procederemo quindi
ad illustrare quelle che sono le API create, le loro funzionalità e attraverso quali metodi accerdervi.Le API sono pensate per
essere integrate sia all'interno di un applicativo che dentro una pipeline CI/CD e per dimostrare ciò è stato creato:
 - un software con una semplice interfaccia e che fornisci degli automatismi per agire sugli snippet. Questo
  astrae le modalità di interazione con le API essendo pensato per un pubblico non geek.

- una pipeline CI/CD che presenta come stadi le attività svolte dalle API

**WARNING 1:** *While running this program your machine will be extremely
vulnerable to attack. You should disconnect from the Internet while using
this program.*  WebGoat's default configuration binds to localhost to minimize
the exposure.

**WARNING 2:** *This program is for educational purposes only. If you attempt
these techniques without authorization, you are very likely to get caught. If
you are caught engaging in unauthorized hacking, most companies will fire you.
Claiming that you were doing security research will not work as that is the
first thing that all hackers claim.*

# Installation instructions:

contact the administrator of this project to obtain the documentation
