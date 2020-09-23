# skill-multicontract-demo

This skill demonstrates how a skill may implement a set of contracts and change its behaviour
depending on the type of the incoming message.

### Defining multiple contracts
A contract must have a clear and definite boundary. This might either be achieved using different
contract files or using namespaces.

**Using multiple contract files**

Within the `skill.yml` file you may specify more than one contract file:

```yaml
...
contract: ["./first", "./second"]
...
```

where as the contract files have the following contents:

```
#src/contract/first.dbs
namespace incoming {
    class Request {
        @NotBlank
        identityId: string
    }
}

namespace outgoing {
    class Response {
      @NotBlank
      qualifiers: [string]
    }
}
```

```
#src/contract/second.dbs
namespace incoming {
    class Request {
        @NotBlank
        a: int
        b: int
    }
}

namespace outgoing {
    class Response {
      @NotBlank
      result: int
    }
}
```

Using this method the contracts will be implicitly merged and wrapped with namespaces representing
their file names.

Regarding the example files the implicitly merged contract does look like this:
```
#namespace representing the file src/contract/first
namespace `first` {
    namespace incoming {
        class Request {
            @NotBlank
            identityId: string
        }
    }

    namespace outgoing {
        class Response {
          @NotBlank
          qualifiers: [string]
        }
    }
}

#namespace representing the file src/contract/second
namespace `second` {
    namespace incoming {
        class Request {
            @NotBlank
            a: int
            b: int
        }
    }
    namespace outgoing {
        class Response {
          @NotBlank
          result: int
        }
    }
}
```
**INFO:** _Please be aware of the grave accent (`)_

**NOTE:** It is ofcourse possible to mix the implementation of custom and default contracts.

The second approach of defining multiple contracts is using a single contract file but specifying the boundary
namespaces yourself:

```yaml
...
contract: ["./multicontract"]
...
```

```
namespace first {
    namespace incoming {
        class Request {
            @NotBlank
            identityId: string
        }
    }

    namespace outgoing {
        class Response {
          @NotBlank
          qualifiers: [string]
        }
    }
}

namespace second {
    namespace incoming {
        class Request {
            @NotBlank
            a: int
            b: int
        }
    }
    namespace outgoing {
        class Response {
          @NotBlank
          result: int
        }
    }
}
```

INFO: In this approach grave accents are only necessary when using special characters.

As you can see either way namespaces are the clear and definite boundary between different contracts.

### Using multiple contacts

When implementing multiple contracts the skill can be considered as the reacting side. 
The client sending the initial request as the acting side.

A client may send a request like this:
```
skills()
   .connect("some-skill-1")
   .evaluate("second", mapOf("a": 1, "b": 2)
```

It is clear that this message is a valid message that fulfils the `second` contract. The client side must specify 
the namespace (or contract) to be used. 

Since the message is valid the skill may now evaluate the message and react accordingly. How exactly this reaction looks
like is decided by the skill developer. Yet the developer must have access to the information which namespace (or contract)
an incoming message (`payload`) implements.

The evaluate method receives two parameters:
* The payload - the actual incoming message
* The evaluation context

The evaluation context contains the information to which contract (or namespace) the current
evaluated message belongs:

```
def evaluate(payload, context):
    namespace = context['namespace']
    if namespace == "second.incoming":
         ...
    elif namespace == "first.incoming":
        ...
    ...
```

Using that information the skill developer can react accordingly and send a matching response.
Constructing the response and attaching the contract (or namespace) information is within the
skill developers responsibility. Now the skill acts as the acting part and must specify which
contract the response message implements.

To do this the response map/dictionary must be constructed accordingly using the following format:
`
{@the_namespace_name: {... actual message ...}}
`


**INFO:** _This might change in future releases_

For our concrete example a response to a message from the namespace `second` might look like this:

```
response = {'@second' : {result: 5}}
```

The complete evaluation function now may look like this:
```
def evaluate(payload, context):
    namespace = context['namespace']
    if namespace == "second.incoming":
         return {'@second': {'result' : 5}}
    else:
        pass
```