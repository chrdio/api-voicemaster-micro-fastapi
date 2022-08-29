from hypothesis import given, strategies as st
import chrdiotypes


info_strategy = st.lists(
        st.tuples(
            st.sampled_from(chrdiotypes.data_enums.enums.NodeIDs),
            st.sampled_from(chrdiotypes.data_enums.enums.ChordSymbolStructures),
        ),
        min_size=8,
        max_size=8
    )
structures_strategy = st.lists(
        st.sampled_from(chrdiotypes.data_enums.enums.ChordIntervalStructures),
        min_size=8,
        max_size=8
    )
cases_strategy = st.lists(st.booleans(), min_size=8, max_size=8)
bases_strategy = st.lists(st.sampled_from(chrdiotypes.data_enums.enums.NotesInt), min_size=8, max_size=8)
key_strategy = st.sampled_from(chrdiotypes.data_enums.enums.NotesInt)
ordering_strategy = st.one_of(
        st.none(), st.sampled_from(chrdiotypes.data_enums.enums.VoiceOrderings)
    )
chsh_strategies = {
    "info": info_strategy,
    "structures": structures_strategy,
    "special_cases": cases_strategy,
    "bases": bases_strategy,
    "key": key_strategy,
    "ordering": ordering_strategy,
}