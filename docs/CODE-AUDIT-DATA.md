# Source audit — coverage for every repository

Snapshot: 2026-11-22T09:48:23.935328+00:00. See [reviewed findings](CODE-AUDIT-2026-11-22.md).

Text read is not human-reviewed or runtime-tested. Parser counts exclude templates; zero candidates is NOT a clean bill of health.
For tree fallback, the source sample is bounded to 120 files. Details of skips and errors are in the accompanying JSON.

| Repository / pinned commit | Method | Regular files inventoried | Text read | Parser checks | Raw candidates | Acquisition errors |
|---|---|---|---|---|---|---|
| [amazon-linux-ami-kernel](https://github.com/devarent/amazon-linux-ami-kernel/tree/d75b09437b953a86581f365d82da003905657a8d) | bounded archive scan | 29 | 24 | 9 | 1 | 0 |
| [apache-kafka-lab](https://github.com/devarent/apache-kafka-lab/tree/7ac2896330d910bd22d754adbb0892542d441296) | bounded archive scan | 9 | 6 | 5 | 0 | 0 |
| [apache-kylin-lab](https://github.com/devarent/apache-kylin-lab/tree/a400ce25e067d683194bfbd09361370128b6d495) | bounded archive scan | 8 | 5 | 2 | 0 | 0 |
| [arya123](https://github.com/devarent/arya123/tree/d144474c8db891bddee5aad898f76bc6a5abab49) | bounded archive scan | 427 | 327 | 103 | 5 | 0 |
| [assembler-addressing-modes-lab](https://github.com/devarent/assembler-addressing-modes-lab/tree/5cb5cd599d6ecbb14e11847c45f401c39446e32b) | bounded archive scan | 15 | 8 | 1 | 0 | 0 |
| [aws-billing-qwen-3-32b](https://github.com/devarent/aws-billing-qwen-3-32b/tree/f5e6ade8c2701389d1a401bbf30be217abde5d6e) | bounded archive scan | 147 | 113 | 38 | 3 | 0 |
| [aws-ec2-web-hosting-part-1](https://github.com/devarent/aws-ec2-web-hosting-part-1/tree/f672325e2b726ba884c0aa169d0734116ebd5692) | bounded archive scan | 162 | 140 | 37 | 0 | 0 |
| [aws-rds](https://github.com/devarent/aws-rds/tree/0746fc97342ad513bc9b921c577eeee97933dc44) | tree-sample (archive exceeded cap) | 7621 | 10 | 1 | 0 | 0 |
| [backend-service-2026](https://github.com/devarent/backend-service-2026/tree/db64855bd2ee9ef9b4dac5598b337f2f2d146b8b) | bounded archive scan | 83 | 71 | 23 | 3 | 0 |
| [bigquery-lab](https://github.com/devarent/bigquery-lab/tree/131ce37c04dbebd594313be4b88337c8abbcbfd5) | bounded archive scan | 9 | 6 | 3 | 0 | 0 |
| [cassandra-lab](https://github.com/devarent/cassandra-lab/tree/eb0855eecde48d9e1ca0874946844dfb34474995) | bounded archive scan | 8 | 5 | 2 | 0 | 0 |
| [chromadb-lab](https://github.com/devarent/chromadb-lab/tree/66b53871a4031843d8235d250ac94a679b03cb67) | bounded archive scan | 8 | 5 | 4 | 0 | 0 |
| [cnn](https://github.com/devarent/cnn/tree/ddb14c3916cff43d44bcf87fb965803f4ef5ec5b) | bounded archive scan | 447 | 28 | 15 | 0 | 0 |
| [cockroachdb-lab](https://github.com/devarent/cockroachdb-lab/tree/e9946bac54f4269a56341ecb6fc88c2cfbeade69) | bounded archive scan | 8 | 5 | 2 | 0 | 0 |
| [convolutional-neural-network](https://github.com/devarent/convolutional-neural-network/tree/17e686d1f1ab7ad4820ebd8c4204ec88ed6378af) | bounded archive scan | 447 | 28 | 15 | 0 | 0 |
| [credit-card-fraud](https://github.com/devarent/credit-card-fraud/tree/56cabf201844ed98b5f2fc9dad7d47425097b662) | bounded archive scan | 16 | 9 | 1 | 0 | 0 |
| [database-labs](https://github.com/devarent/database-labs/tree/b0c22b91a679c64a8524d5a637e18d5923934449) | bounded archive scan | 11 | 6 | 4 | 0 | 0 |
| [database-labs-demo](https://github.com/devarent/database-labs-demo/tree/84ab5618104e14b51f4f430c6a00e13ebf918a5d) | bounded archive scan | 27 | 14 | 9 | 0 | 0 |
| [databend-lab](https://github.com/devarent/databend-lab/tree/5ddcec42da5e5df85ea402432632d7ec25554c99) | bounded archive scan | 8 | 5 | 2 | 0 | 0 |
| [databricks-sql-lab](https://github.com/devarent/databricks-sql-lab/tree/d12b163fb5a0e2398699df7c07a9d8b8cb5dffe3) | bounded archive scan | 7 | 4 | 0 | 0 | 0 |
| [dbx](https://github.com/devarent/dbx/tree/363ab9a4c1856cc18cf2d87ab8bec6e2fdfd82c5) | tree-sample (archive exceeded cap) | 8481 | 120 | 56 | 1 | 0 |
| [devarent](https://github.com/devarent/devarent/tree/71b700de127c0e470f569482cda2e93c1855dd9c) | bounded archive scan | 25 | 12 | 2 | 0 | 0 |
| [devhub](https://github.com/devarent/devhub/tree/426bd29b555e28bf778bcdd7725c5e7857757bc0) | bounded archive scan | 1871 | 1477 | 86 | 1 | 0 |
| [devhub-modernized](https://github.com/devarent/devhub-modernized/tree/6fa12781b369fa8dd641d4b313ec0edfa1327a2c) | bounded archive scan | 1092 | 858 | 65 | 1 | 0 |
| [devops-platform-2026](https://github.com/devarent/devops-platform-2026/tree/a5cee0780ba87aa9d0699832a968c26b25771c5c) | bounded archive scan | 54 | 49 | 11 | 0 | 0 |
| [elasticsearch-lab](https://github.com/devarent/elasticsearch-lab/tree/0f8e18f323da3a1128ca1f98c4903b90684b47b2) | bounded archive scan | 9 | 6 | 5 | 0 | 0 |
| [email-spam-detector](https://github.com/devarent/email-spam-detector/tree/da105b0b95999bead7799371bd8be113e9621120) | bounded archive scan | 22 | 12 | 4 | 0 | 0 |
| [firebird-lab](https://github.com/devarent/firebird-lab/tree/3d38dec58588ddc0c5df4b7dfba9fb660c1f8802) | bounded archive scan | 8 | 5 | 2 | 0 | 0 |
| [hris-itk-laravel](https://github.com/devarent/hris-itk-laravel/tree/0401f1cf48dc493e26e7bbd6e301e312f9536d3d) | bounded archive scan | 186 | 163 | 4 | 0 | 0 |
| [ibm-db2-lab](https://github.com/devarent/ibm-db2-lab/tree/c35337c6987714e98831cbe2ae8884029cedb433) | bounded archive scan | 8 | 5 | 2 | 1 | 0 |
| [influxdb-lab](https://github.com/devarent/influxdb-lab/tree/890baed387f90f6b9ea7a786228f6862f774a313) | bounded archive scan | 9 | 5 | 4 | 0 | 0 |
| [intelligent-security-lab](https://github.com/devarent/intelligent-security-lab/tree/025e41067a256371d08890a3a0c127de93dc626d) | bounded archive scan | 39 | 33 | 17 | 0 | 0 |
| [intersystems-iris-lab](https://github.com/devarent/intersystems-iris-lab/tree/0bdba2998efb524ac59ff6ec3b8917d7ebdab621) | bounded archive scan | 8 | 5 | 2 | 0 | 0 |
| [jailbreak-root](https://github.com/devarent/jailbreak-root/tree/307bae08f93906dff85beb1b0e73f2a0fcf05d07) | bounded archive scan | 31 | 19 | 12 | 0 | 0 |
| [jdbc-lab](https://github.com/devarent/jdbc-lab/tree/436436c473ac353c8ac7e7399f7083b564c177ec) | bounded archive scan | 11 | 7 | 3 | 0 | 0 |
| [k8s](https://github.com/devarent/k8s/tree/41775f0d7e4efe5ee0d1bc0c4b39a0b8dacac05e) | bounded archive scan | 16 | 13 | 6 | 0 | 0 |
| [lab-3-advanced-arithmetic](https://github.com/devarent/lab-3-advanced-arithmetic/tree/e88f09b54de136dbd3e6b4e24dab60120fe512b6) | bounded archive scan | 37 | 17 | 9 | 0 | 0 |
| [lambda-localstack-lab](https://github.com/devarent/lambda-localstack-lab/tree/e3ec803759c35220ac61334bcd89c2ec1981dceb) | bounded archive scan | 39 | 30 | 16 | 0 | 0 |
| [laravel](https://github.com/devarent/laravel/tree/dcc46b55993deb4606ec6ff259cf67b2a27ebdcb) | bounded archive scan | 64 | 39 | 2 | 0 | 0 |
| [laravel-modernized](https://github.com/devarent/laravel-modernized/tree/96fba8bd0c5dd9015fa156b57977d62f6eaa8605) | bounded archive scan | 58 | 34 | 2 | 0 | 0 |
| [localstack-lambda-copy](https://github.com/devarent/localstack-lambda-copy/tree/1bab66eaf5baa766586153fafb6e17a9a862804e) | bounded archive scan | 39 | 30 | 16 | 0 | 0 |
| [machine-learning-dicoding](https://github.com/devarent/machine-learning-dicoding/tree/07492a775afa61151a2b0a0efc9ef94726e5b6e9) | bounded archive scan | 30 | 14 | 7 | 0 | 0 |
| [mariadb-practicum](https://github.com/devarent/mariadb-practicum/tree/7a20f097b68a66b7df193e37831dcf3722412426) | bounded archive scan | 18 | 14 | 5 | 2 | 0 |
| [microprocessor-microcontroller-lab](https://github.com/devarent/microprocessor-microcontroller-lab/tree/785281a1a40e92fd0232391f44f79db054831925) | bounded archive scan | 21 | 8 | 1 | 0 | 0 |
| [ml-pipeline-end-to-end](https://github.com/devarent/ml-pipeline-end-to-end/tree/23a1da6a4f8a990dfd227b00e99059efca92a9cb) | bounded archive scan | 33 | 13 | 4 | 0 | 0 |
| [mongodb-practicum](https://github.com/devarent/mongodb-practicum/tree/de03eae3119e1ce8945562760f10cb2b19acec94) | bounded archive scan | 14 | 10 | 5 | 2 | 0 |
| [neo4j-lab](https://github.com/devarent/neo4j-lab/tree/5321a5fcb89e59d9a0b51e9756bce64446c7642c) | bounded archive scan | 8 | 3 | 2 | 0 | 0 |
| [nextjs-aws-production](https://github.com/devarent/nextjs-aws-production/tree/dc19a0a2b1346d286e4f05b751a38bae93d18d8f) | bounded archive scan | 56 | 45 | 17 | 2 | 0 |
| [nginx](https://github.com/devarent/nginx/tree/79fb7f981fc99ba8f624a627821e2bef94935a4a) | bounded archive scan | 11 | 8 | 1 | 0 | 0 |
| [qa-automation-2026](https://github.com/devarent/qa-automation-2026/tree/e87fbdb052416f8a117e9774ec781d9d62e82d8b) | bounded archive scan | 59 | 51 | 5 | 0 | 0 |
| [qdrant-lab](https://github.com/devarent/qdrant-lab/tree/a2ab3681e31817d59e448bd995a05718574480ac) | bounded archive scan | 9 | 6 | 5 | 0 | 0 |
| [quantum-hybrid-diffusion-models](https://github.com/devarent/quantum-hybrid-diffusion-models/tree/75f263474ebf701106ef94568efb95b78f60ba1e) | bounded archive scan | 1405 | 808 | 298 | 3 | 0 |
| [quantum-hybrid-ml-databricks-snowflake](https://github.com/devarent/quantum-hybrid-ml-databricks-snowflake/tree/6fb2d64a410f8a3af279a411be78c3a98ff42646) | bounded archive scan | 1405 | 808 | 298 | 3 | 0 |
| [quantum-hybrid-ml-databricks-snowflake-modernized](https://github.com/devarent/quantum-hybrid-ml-databricks-snowflake-modernized/tree/304c42600d42da4142583e9a9d869bfe84b457e6) | bounded archive scan | 1405 | 808 | 298 | 3 | 0 |
| [react](https://github.com/devarent/react/tree/70460d245de02334da41996ae9eb56ef6430ba7b) | bounded archive scan | 7284 | 6830 | 203 | 17 | 0 |
| [react-modernized](https://github.com/devarent/react-modernized/tree/6fc80e1826c18d49a792de1bc96e4fae1f41e8af) | bounded archive scan | 7284 | 6830 | 203 | 17 | 0 |
| [redis-lab](https://github.com/devarent/redis-lab/tree/8751fbdf22c38bececf271c194c93f2a34ab11bd) | bounded archive scan | 8 | 4 | 3 | 0 | 0 |
| [redshift-lab](https://github.com/devarent/redshift-lab/tree/d26a000bd167229a9a5229514f3c281c719bb1de) | bounded archive scan | 7 | 4 | 0 | 0 | 0 |
| [repo-atlas-next](https://github.com/devarent/repo-atlas-next/tree/0c85f974531369796edfa90daeb0175042fe0314) | bounded archive scan | 62 | 40 | 10 | 1 | 0 |
| [scripts](https://github.com/devarent/scripts/tree/c76f2c1812c9229bf270503b0fcc9eaf1cea76d7) | bounded archive scan | 13 | 9 | 2 | 0 | 0 |
| [self-concept-reflection](https://github.com/devarent/self-concept-reflection/tree/b69c827936f7d6aed6d05cedd659b10864b9c1e9) | bounded archive scan | 14 | 8 | 1 | 0 | 0 |
| [sensor-hewan](https://github.com/devarent/sensor-hewan/tree/4e25021ea7584bd6f8489ed207fa1e7eba3bc9e2) | bounded archive scan | 447 | 28 | 15 | 0 | 0 |
| [snowflake-databricks](https://github.com/devarent/snowflake-databricks/tree/6baac9daf9c5837ea8a20d274060ce505137f124) | bounded archive scan | 15 | 10 | 1 | 0 | 0 |
| [snowflake-lab](https://github.com/devarent/snowflake-lab/tree/5d22753334fdf9996f2a7565712e96978bee2412) | bounded archive scan | 7 | 4 | 0 | 0 | 0 |
| [sql-server-lab](https://github.com/devarent/sql-server-lab/tree/e730f53b74c18118df24a36f103de4545fe3765a) | bounded archive scan | 8 | 5 | 2 | 0 | 0 |
| [tdengine-lab](https://github.com/devarent/tdengine-lab/tree/f5f6571e530968f96bba781373007fe5048bb64b) | bounded archive scan | 8 | 5 | 2 | 0 | 0 |
| [teradata-lab](https://github.com/devarent/teradata-lab/tree/28e80e8bef58a446322c02c2caf63db9007014aa) | bounded archive scan | 6 | 3 | 0 | 0 | 0 |
| [terraform-databricks-sra](https://github.com/devarent/terraform-databricks-sra/tree/a9db178ca70c61c88a53fb84ae6856050ed57151) | bounded archive scan | 401 | 337 | 26 | 3 | 0 |
| [terraform-databricks-sra-modernized](https://github.com/devarent/terraform-databricks-sra-modernized/tree/de90425508fac1f962e1809253f6190f808be326) | bounded archive scan | 403 | 339 | 27 | 3 | 0 |
| [ui](https://github.com/devarent/ui/tree/1244c5d3301be08757f1f0244751e6eed7e3ef47) | bounded archive scan | 6414 | 5576 | 1099 | 15 | 0 |
| [ui-modernized](https://github.com/devarent/ui-modernized/tree/919521aea6bcfc4d58c400a1e1e46f6adb328a1a) | bounded archive scan | 4792 | 4120 | 1058 | 15 | 0 |
| [unit-testing-practice](https://github.com/devarent/unit-testing-practice/tree/9a1dd66e5784cc85458dfd761a70c7057803c543) | bounded archive scan | 20 | 13 | 3 | 0 | 0 |
| [uts-ec2-amazon-linux](https://github.com/devarent/uts-ec2-amazon-linux/tree/af8f998ab1b86e12ab25945b26e3dd390d9d16f8) | bounded archive scan | 369 | 273 | 101 | 5 | 0 |
| [vertica-lab](https://github.com/devarent/vertica-lab/tree/7b109880d292a2bbd3ce77b9c807b51f1afa9cf1) | bounded archive scan | 6 | 3 | 0 | 0 | 0 |
| [victoriametrics-lab](https://github.com/devarent/victoriametrics-lab/tree/8eba4046998061ec08bc2614af516830d2a2ba8c) | bounded archive scan | 9 | 6 | 5 | 0 | 0 |
| [week-4-programming-fundamentals](https://github.com/devarent/week-4-programming-fundamentals/tree/643bec8526117077ddf55fa3da135de297781d7d) | bounded archive scan | 74 | 34 | 13 | 0 | 0 |
| [wokwi](https://github.com/devarent/wokwi/tree/b1a7265202b3334bf96bc8a96508cb8f7f0f67be) | bounded archive scan | 12 | 10 | 2 | 0 | 0 |
| [zerobus-sdk](https://github.com/devarent/zerobus-sdk/tree/a4d739bfa2913f7fe0d648cd98116fd569ed5cfe) | bounded archive scan | 777 | 571 | 94 | 0 | 0 |
| [zerobus-sdk-modernized](https://github.com/devarent/zerobus-sdk-modernized/tree/f3fe2c61ded6bf55d22400fe16dea7fb420b87b0) | bounded archive scan | 777 | 570 | 92 | 0 | 0 |
