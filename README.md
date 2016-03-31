# jacis
Just Another Continuous Integration System


# Quick intro

* init.ci

```yaml

tasks:
    - sync-deliveries
    - generate-project

sync-deliveries:
    - sync: 
        repo: svn://https://github.com/ddolzhenko/TestGit/
        path: test/tree-1
        tag:  v1.0   
        to:   tools/test1
    
    - sync: 
        repo: git://https://github.com/ddolzhenko/TestGit.git
        path: test/tree-1/foo.txt
        tag: v1.0
        to: tools/test1
    
    - sync: 
        repo: p4://123.222.0.12:6500
        path: //ht-cy48//project/apps/config/mocca 
        tag:  head 
        to:   deliveries/

   

    
```