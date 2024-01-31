def parse_unused(chains, chain_name):
    unused_policy=[]
    one_kind_chain = chains[chain_name]
    for chain in one_kind_chain: 
        if((chain["bytes"]=='0')):
            unused_policy.append(chain)
    chains[chain_name] = unused_policy
    return chains
