# Metropolis - Montecarlo

## Pasos para correr el proyecto
1. Ubicarse en la carpeta fuente
```bash
cd metropolis
```

2. Compilar
```bash
mvn clean package
```
3. Correr el archivo jar
```bash
cd target
java -jar metropolis-1.0-SNAPSHOT.jar -Dn=50 -Dp=0.1 
```

## Parametros de la VM
- `-Dn`: Es la dimension de la grilla
- `-Dp`: Es la probabilidad de que un individuo cambie su estado oponiendose a los vecinos
